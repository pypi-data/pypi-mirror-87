import os.path
import logging
import pickle

from googleapiclient.discovery import build as build_api
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from oauthlib.oauth2.rfc6749.errors import \
    OAuth2Error as _OAuth2Error, AccessDeniedError

from .messages import Messages
from .common import Cacheable
from .utils import nat, is_seq_like


logger = logging.getLogger(__name__)


class OAuth2Error(_OAuth2Error):
    pass

class Gmail(Cacheable):
    # If modifying these scopes, use a new token pickle file
    scopes = ['https://www.googleapis.com/auth/gmail.readonly']
    _holds = Messages

    def __init__(self, client_creds_file, token_file=None):
        '''Search and caches messages

        client_creds_file: JSON file containing OAuth client
            credentials
        token_file: Previously saved token pickle file containing user
            access token. If it doesn't exist it is created.
        '''

        super().__init__()
        self.api = self._get_api(client_creds_file, token_file)

    def fetch(self,
              preferred_mime_type=None,
              query=None,
              id_range=None,
              **search_kwargs):
        '''Search in Gmail for messages
        - query is a gmail query to filter messages
        - id_range can be an integer or a tuple of min and max
          integers to select specific emails, starting at 1 with the
          most recent one; negative integers count from the oldest.
          For example (1,10) will select the latest 10 only.
        - Any search_kwargs are passed to each resulting Message to
          find a string within it, see Message.search. Results can be
          looked up with Message.last_search.

        Returns the found emails (matching query) which match the
        search (or all found emails if no search was given).
        '''

        def is_in_range(m_id, id_range):
            return m_id >= id_range[0] and m_id <= id_range[1]

        def adjust_id_range(id_range, n_total):
            if id_range is None:
                return (1, n_total)
            if isinstance(id_range, (str, int)):
                id_range = (id_range, id_range)
            id_range = (int(id_range[0]), int(id_range[1]))
            adj = lambda x: x if x > 0 else n_total + x + 1
            return tuple(sorted(map(adj, id_range)))

        if not is_seq_like(id_range) and \
                not isinstance(id_range, (type(None), str, int)):
            raise TypeError('id_range must be an int or a sequence')
        elif is_seq_like(id_range) and len(id_range) != 2:
            raise ValueError(
                'id_range must be an int or a two-item sequence')

        cache_key = query
        is_mod = False
        new_query = None
        if cache_key not in self:
            # never looked up, fetch all
            is_mod = True
            new_query = query
            self.new_cache(cache_key)
            logger.debug(
                'No cached search results for email query {}'.format(
                    query))
        elif query is not None and ' after:' not in query and \
                not query.startswith('after:'):
            is_mod = True
            # no time was explicitly given, but we've previously
            # fetched this query, so just get the new emails since
            # then
            new_query = '{}after:{:.0f}'.format(
                '' if query is None else query + ' ',
                self.last_modified(cache_key))

        n_total = len(self[cache_key])
        if is_mod:
            # fetch the messages
            raw_messages = self._get_raw_msgs(query=new_query)
            n_new = len(raw_messages)
            n_total += n_new
            logger.debug('Found {} new messages'.format(n_new))
            for msg in raw_messages:
                # store a dummy one now
                self.new_cache_item(
                    cache_key,
                    fetcher=self._get_raw_msg,
                    msg_id=msg['id'],
                    preferred_mime_type=preferred_mime_type)

        # filter based on id_range and search_kwargs
        result = Messages()
        logger.debug('Found {} total messages'.format(n_total))
        assert n_total == len(self[cache_key])
        _id_range = adjust_id_range(id_range, n_total)
        logger.debug('Taking messages in range {}'.format(_id_range))

        for m_id, msg in enumerate(self[cache_key], start=1):
            if not is_in_range(m_id, _id_range):
                continue
            if not msg.fetched:
                msg.fetch()
            if search_kwargs and not msg.search(**search_kwargs):
                continue
            result.add(msg)
        return result

    def load_cache(self, cache_file):
        '''Load a message cache from a file'''

        with open(cache_file, 'rb') as cache_fh:
            self._search_cache = pickle.load(cache_fh)

    def save_cache(self, cache_file):
        '''Save the current message cache to a file'''

        with open(cache_file, 'wb') as cache_fh:
            pickle.dump(self._search_cache, cache_fh)

    def _get_api(self, client_creds_file, token_file):
        token = None
        if token_file is not None and os.path.exists(token_file):
            with open(token_file, 'rb') as token_fh:
                token = pickle.load(token_fh)

        if token and token.expired and token.refresh_token:
            token.refresh(Request())
        elif not token or not token.valid:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_creds_file, self.scopes)

            try:
                # TODO investigate: sometimes on MacOS giving port
                # 0 doesn't work (nothing is listening on the random
                # port)
                token = flow.run_local_server(port=0)
            except AccessDeniedError as e:
                logger.error('Client refused to grant permission')
                raise OAuth2Error(e)
            except _OAuth2Error as e:
                logger.error('Error: {!s}'.format(e))
                raise OAuth2Error(e)

        if token_file is not None:
            with open(token_file, 'wb') as token_fh:
                pickle.dump(token, token_fh)

        return build_api('gmail', 'v1', credentials=token)

    def _get_raw_msgs(self, query=None):
        def get_page(page_token):
            logger.trace(
                'Fetching messages {}, pageToken={}'.format(
                    query, page_token))
            return self.api.users().messages().list(
                userId='me',
                pageToken=page_token,
                q=query).execute()

        messages = []
        first = True
        page_token = None
        while first or page_token:
            results = get_page(page_token)
            messages.extend(results.get('messages', []))
            page_token = results.get('nextPageToken')
            first = False
        return messages

    def _get_raw_msg(self, msg_id):
        logger.debug('Fetching msg {}'.format(msg_id))
        return self.api.users().messages().get(
            userId='me', id=msg_id).execute()
