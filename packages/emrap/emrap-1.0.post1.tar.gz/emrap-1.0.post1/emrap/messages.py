import logging
import re
from functools import partial
from datetime import datetime
import base64
from http_parser.util import IOrderedDict

from .common import Searchable, Sortable, Cacheable, \
    SortedUniqueContainer
from .utils import str_trunc, str_to_re_flags
from .extracts import SortedExtracts, OrderedExtracts


logger = logging.getLogger(__name__)


class Message(Cacheable, Searchable, Sortable):
    _holds = SortedExtracts
    _extract_type = OrderedExtracts

    def __init__(self,
                 msg=None,
                 fetcher=None,
                 msg_id=None,
                 preferred_mime_type=None):
        '''If message is given, it is parsed

        fetcher is a callable which will fetch the raw message to be
        parsed when the fetch method is used; msg_id will be
        passed to it if given
        '''

        if msg is None:
            if None in [msg_id, fetcher]:
                raise TypeError(
                    'msg_id and fetcher must both be given')
        elif None not in [msg_id, fetcher]:
            raise TypeError(
                'msg cannot be given together when fetcher '
                'or msg_id are given')

        super().__init__()
        self._msg = None
        self._fetcher = fetcher
        self._preferred_mime_type = preferred_mime_type
        self._last_cache_key = None

        self.id = msg_id
        self.mime_type = None
        self.headers = IOrderedDict()
        self.body = None
        self.subject = None
        self.snippet = None
        self.timestamp = None
        self.to_address = None
        self.from_address = None
        self.attachments = []  # TODO

        if msg is not None:
            self.parse(msg)
            logger.trace(
                'Message subject = "{}", snippet = "{}"'.format(
                    self.subject, self.snippet))

    @property
    def fetched(self):
        return self._msg is not None

    @property
    def time(self):
        if self.timestamp is None:
            return None
        return datetime.fromtimestamp(
            self.timestamp).strftime('%d %b %Y %H:%M:%S')

    @property
    def _comparables(self):
        # sort in descending order by ID (which will also sort in
        # descending order by time)
        return -int(self.id, base=16)

    def parse(self, msg):
        '''Initializes the message with the given content'''

        if self.fetched:
            raise RuntimeError('Message already parsed')
        self._parse(msg)

    def fetch(self, fetcher=None):
        if fetcher is None:
            fetcher = self._fetcher
        self.parse(fetcher(self.id))

    def search(self, regex, where=['subject', 'body'], **kwargs):
        '''Search within the body and/or subject for the given regex

        See Searchable._search for description of the arguments
        '''

        return self._search(regex, where=where, **kwargs)

    @property
    def last_search(self):
        if self._last_cache_key is None:
            raise RuntimeError('No search has been performed yet')
        return self[self._last_cache_key]

    def _get_parts(self, payload=None):
        if payload is None:
            payload = self._msg['payload']
        if payload['filename']:  # TODO
            logger.trace('Skipping attachment')
            return []

        logger.trace('Processing payload')
        body = payload['body']
        mime = payload['mimeType']
        result = []
        try:
            data = body['data']
        except KeyError:
            logger.trace('Body is multi-part')
            for p in payload['parts']:
                result.extend(self._get_parts(p))
        else:
            logger.trace('Body is single-part')
            result.append({'data': data, 'mimeType': mime})
        return result

    def _parse(self, msg):
        def get_address(value):
            m = re.search(
                '[a-z0-9.+_-]+@[]a-z0-9._-]+', value, flags=re.I)
            if m is None:
                logger.warning(
                    "Can't determine email address from {}".format(
                        value))
                return value
            return m.group(0)

        def decode_data(data):
            altchars = None
            if '-' in data or '_' in data:
                altchars = '-_'
            return base64.b64decode(data, altchars=altchars).decode(
                'utf-8', errors='backslashreplace')

        self._msg = msg
        self.id = msg['id']
        self.snippet = self._msg.get('snippet', '')
        self.timestamp = float(self._msg['internalDate']) / 1000
        for hdr in self._msg['payload']['headers']:
            self.headers[hdr['name']] = hdr['value']
        self.subject = self.headers.get('Subject', '')
        self.to_address = get_address(self.headers.get('To', ''))
        self.from_address = get_address(self.headers.get('From', ''))

        parts = self._get_parts()
        for p in parts:
            self.body = decode_data(p['data'])
            self.mime_type = p['mimeType']
            if p['mimeType'] == self._preferred_mime_type:
                break

    def __repr__(self):
        return '{}([{} at {}] {}: {})'.format(
            self.__class__.__name__,
            self.id,
            self.time,
            str_trunc(str(self.subject), 20),
            str_trunc(str(self.snippet), 30))

    def __str__(self):
        return self.__repr__()

class Messages(SortedUniqueContainer):
    _holds = Message

    def get(self,
            to_address=None,
            from_address=None,
            before=None,
            after=None,
            **search_kwargs):
        '''Returns all messages that match the queries

        search_kwargs are passed to each message's search method and
        if nothing is found, the message is omitted from the result.
        Result for each can be looked up using Message.last_search
        '''

        result = self.__class__()
        for m in self:
            if to_address not in [None, m.to_address]:
                continue
            if from_address not in [None, m.from_address]:
                continue
            if before is not None and before < m.timestamp:
                continue
            if after is not None and after > m.timestamp:
                continue
            if search_kwargs and not m.search(**search_kwargs):
                continue
            result.add(m)
        return result
