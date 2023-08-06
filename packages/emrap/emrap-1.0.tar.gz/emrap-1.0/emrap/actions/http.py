# TODO support random request_id substitutions

import logging
import re
from random import randint
import os.path
from time import sleep
from argparse import ArgumentParser
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor, \
    as_completed as futures_as_completed

from .. import setup_logger
from ..gmail import Gmail
from ..http import HttpRequest, HttpRequestRaw
from ..utils import nat, smart_open, decode
from ..extracts import ExtractDirectives, ExtractDirectivesContainer
from .common import ArgumentDefaultsSmartHelpFormatter

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


logger = logging.getLogger(__name__)


class HttpExtractDirectives(ExtractDirectives):
    _defaults = {
        # if there are no defaults, then it is required
        'stages': ['pre', 'fetch', 'post'],
        'where': ['subject', 'raw_headers', 'body', 'content'],
        'regex_group': 0,
        'regex_flags': '',
        'default': 'NOT FOUND',
    }
    _value_constraints = {
        'stages': ['pre', 'fetch', 'post'],
        'where': [
            'to_address', 'from_address', 'subject', 'body',  # email
            'raw_headers', 'content',                 # HTTP response
            'time'],                                         # common
    }

class HttpExtractDirectivesContainer(ExtractDirectivesContainer):
    _holds = HttpExtractDirectives

class HttpAutomator:
    def __init__(self):
        self.args = None
        self.gmail = None
        self.extract_directives = HttpExtractDirectivesContainer()

        self.parser = ArgumentParser(
            formatter_class=ArgumentDefaultsSmartHelpFormatter,
            add_help=False,
            description='''
            HTTP request automator with email search capability.
            An automation app to send HTTP requests which may generate
            an email, search in gmail and extract value, then
            optionally send more requests. Good for automarting
            password resets for example. It can be used just to search
            in emails. Supports dynamic text substitution with values
            extracted from previous responses or emails.
            ''')

        auth_parser = self.parser.add_argument_group(
            'Options related to authentication')
        auth_parser.add_argument(
            '--creds-file', '-c', required=True,
            help='JSON file containing OAuth client credentials')
        auth_parser.add_argument(
            '--token-file', '-t',
            help='''Previously saved token pickle file containing user
            access token. If it doesn't exist it is created.''')

        filter_parser = self.parser.add_argument_group(
            'Options related to filtering emails')
        filter_parser.add_argument(
            '--query', '-q',
            help='''Search query to filter emails. See
            https://support.google.com/mail/answer/7190?hl=en.''')
        id_filter_parser = \
            filter_parser.add_mutually_exclusive_group()
        id_filter_parser.add_argument(
            '--latest', '-l', dest='range', action='store_const',
            const=1, help='Take only the latest email that matches.')
        id_filter_parser.add_argument(
            '--earliest', '-e', dest='range', action='store_const',
            const=-1,
            help='Take only the earliest email that matches.')
        id_filter_parser.add_argument(
            '--range', '-r', nargs=2, metavar='MIN MAX',
            help='''Take only emails number MIN to MAX (including)
            when sorted in descending order by time.''')

        regex_parser = self.parser.add_argument_group(
            '''Options related to extracting text from responses or
            email''')
        regex_parser.add_argument(
            '--extracts', '-E', nargs='+', action='append',
            metavar='directive:value [directive:value ...]',
            help='''This specifies how and where to search for and
            extract text and gives a name each extracted set of values
            that can be used to substitute in HTTP requests. The flag
            is given once per substitution definition and can be given
            as many times as needed. It takes one or more of the
            following directives (each as a separate argument). There
            should not be a space around either side of the colon
            unless intended, e.g. if the 'default' directive value
            should contain leading spaces.

            \\newline
            \\tabname:{unique name} HTTP requests can then use
            \\newline
            \\tab\\tab'{%%name%%}' which will be substituted by
            \\newline
            \\tab\\tabwhatever matched name. By default the first
            \\newline
            \\tab\\tabmatch is taken, specify another one by appending
            \\newline
            \\tab\\tab_N, e.g. '{%%name_2%%}' for the second one.
            \\newline
            \\tab\\tabThe results table will list all matches along
            \\newline
            \\tab\\tabwith the name regardless if any HTTP requests
            \\newline
            \\tab\\tabwere supplied.

            \\newline
            \\tabstages:pre|fetch|post fetch matches in emails and
            \\newline
            \\tab\\tabpre|post in pre- or post- email search. If not
            \\newline
            \\tab\\tabgiven, then all three stages are searched.

            \\newline
            \\tabwhere:to_address,from_address,subject,raw_headers,body,content,time
            \\newline
            \\tab\\tabAny of these can be given. to/from_address,
            \\newline
            \\tab\\tabsubject and body apply to emails, raw_headers
            \\newline
            \\tab\\taband content to HTTP responses, time applies to
            \\newline
            \\tab\\tabboth. Defaults to search headers/subject and
            \\newline
            \\tab\\tabbody/content.

            \\newline
            \\tabregex:{arbitrary regex} Emails (stage fetch) are
            \\newline
            \\tab\\tabsearched in descending order of time and
            \\newline
            \\tab\\tabrequests (stages pre and post) are searched in
            \\newline
            \\tab\\taborder they were received.

            \\newline
            \\tabregex_group:{number} Default is to take the whole
            \\newline
            \\tab\\tabmatch.

            \\newline
            \\tabregex_flags:{flags} One letter per flag, e.g. IM for
            \\newline
            \\tab\\tabcase Insensitive and Multiline (see doc on
            \\newline
            \\tab\\tabpython.re).

            \\newline
            \\tabdefault:{arbitrary text} Text to use if regex
            \\newline
            \\tab\\tabdoesn't match. Default is empty.
            ''')
        regex_parser.add_argument(
            '--mime-type', '-M', default='text/plain',
            help='''Preferred MIME type to search in. Only applies to
            searching in multipart emails.''')

        request_parser = self.parser.add_argument_group(
            '''Options related to sending requests. HTTP requests are
            read from text files as raw HTTP requests. Dynamic
            replacements are supported.''')
        pre_search_request_parser = \
            request_parser.add_mutually_exclusive_group()
        pre_search_request_parser.add_argument(
            '--pre-search', '-b', nargs='+',
            help='''List of files to send as HTTP requests before
            email search. Requests will be sent synchronously, one
            after the other.''')
        pre_search_request_parser.add_argument(
            '--pre-search-async', '-B', nargs='+',
            help='''List of files to send as HTTP requests before
            email search. Requests will be sent by concurrent
            threads.''')

        post_search_request_parser = \
            request_parser.add_mutually_exclusive_group()
        post_search_request_parser.add_argument(
            '--post-search', '-a', nargs='+',
            help='''List of files to send as HTTP requests after email
            search. Executed for each email that matched the search.
            Requests will be sent synchronously, one after the
            other.''')
        post_search_request_parser.add_argument(
            '--post-search-async', '-A', nargs='+',
            help='''List of files to send as HTTP requests after email
            search. Executed for each email that matched the search.
            Requests will be sent by concurrent threads.''')

        origin_request_parser = \
            request_parser.add_mutually_exclusive_group()
        origin_request_parser.add_argument(
            '--origin', '-O',
            help='''Specify origin as {protocol}://{host}[:{port}].
            This overrides the Host header for all requests.''')
        origin_request_parser.add_argument(
            '--is-ssl', help='''Use SSL. This overrides guessing from
            the port number in the Host header for all requests. If no
            port is present in the Host header, it defaults to HTTP on
            port 80.''')

        request_parser.add_argument(
            '--max-threads', type=nat, default=5,
            help='Maximum number of threads to start in async mode.')
        request_parser.add_argument(
            '--timeout', '-T', type=nat,
            help='Timeout in seconds for response')
        request_parser.add_argument(
            '--min-wait', '-w', default=0, type=nat,
            help='Min seconds to wait before sending next request.')
        request_parser.add_argument(
            '--max-wait', '-W', default=0, type=nat,
            help='Max seconds to wait before sending next request.')

        status_code_request_parser = \
            request_parser.add_mutually_exclusive_group()
        status_code_request_parser.add_argument(
            '--success-codes', default=['2XX'], nargs='+',
            metavar='2XX 3XX', help='''List of codes considered
            a success. X matches any digit.''')
        status_code_request_parser.add_argument(
            '--fail-codes', nargs='+', metavar='4XX 5XX',
            help='''List of codes considered a failure. X matches any
            digit.''')

        request_parser.add_argument(
            '--retry', '-R', type=nat, default=0, nargs='?', const=1,
            metavar='N', help='''Retry N times on failed response.
            N defaults to 1 if omitted.''')
        request_parser.add_argument(
            '--no-verify', dest='verify_ssl', default=True,
            action='store_false',
            help='''Do not verify SSL certificate and ignore
            warnings.''')
        request_parser.add_argument(
            '--no-redirect', dest='allow_redirects', default=True,
            action='store_false',
            help='''Do not follow redirections.''')

        misc_request_parser = \
            request_parser.add_mutually_exclusive_group()
        misc_request_parser.add_argument(
            '--proxy', '-x',
            help='''HTTP proxy to use in the format of
            {hostname}:{port}.''')
        misc_request_parser.add_argument(
            '--raw-socket', '-S', default=False, action='store_true',
            help='''Send the request content over a raw IPv4 socket.
            Default is to use python's requests package which may add
            some headers as well as change Content-Length. Using
            a proxy, following redirections and SSL verification is
            not supported when using raw sockets.''')

        display_parser = self.parser.add_argument_group(
            'Options related to displaying output')
        display_parser.add_argument(
            '--output', '-o', help='''Text file to print summary table
            to. '-' means standard output.''')

        global_parser = self.parser.add_argument_group(
            'Global options ')
        request_parser.add_argument(
            '--repeat', '-n', default=1, type=nat,
            help='''How many times to repeat each
            [request->]search[->request cycle]. Extracted text from
            previous cycles is available for substitution.''')
        global_parser.add_argument(
            '--cache-file', '-C',
            help='''Previously saved cache to restore from. If it
            doesn't exist it is created.''')
        global_parser.add_argument(
            '--verbose', '-v', action='count',
            help='''Be verbose. Can be given multiple times to
            increase verbosity. Twice is for debugging, three times is
            to flood your screen with virtually useless
            information.''')
        global_parser.add_argument(
            '--help', '-h', action='help',
            help='Show this help message and exit.')

    @property
    def enabled_stages(self):
        if self.args is None:
            return []
        stages = ['fetch']  # always enabled
        if self.args.pre_search or self.args.pre_search_async:
            stages.insert(0, 'pre')
        if self.args.post_search or self.args.post_search_async:
            stages.append('post')
        return stages

    def run(self, args=None):
        self.args = args
        if args is None:
            self.args = self.parser.parse_args()
        logger.trace(self.args)
        self._parse_extract_directives()

        setup_logger(self.args.verbose)

        self.gmail = Gmail(self.args.creds_file,
                           token_file=self.args.token_file)
        if self.args.cache_file is not None and \
                os.path.exists(self.args.cache_file):
            self.gmail.load_cache(self.args.cache_file)

        logger.debug('Enabled stages: {}'.format(self.enabled_stages))
        for n in range(self.args.repeat):
            if n > 0:
                self._sleep()
            self._run_once()

        self._print()

        if self.args.cache_file is not None:
            self.gmail.save_cache(self.args.cache_file)

    def _run_once(self):
        self._send_requests('pre')
        self._fetch()
        self._send_requests('post')

    def _sleep(self):
        sleep(randint(self.args.min_wait, self.args.max_wait))

    def _parse_extract_directives(self):
        if self.args.extracts is None:
            return
        for ds in self.args.extracts:
            try:
                kwargs = dict([item.split(':', maxsplit=1)
                               for item in ds])
            except ValueError as e:
                raise ValueError(
                    ('Invalid extract directive:value pair: '
                     '{!s}').format(e))
            ed = self.extract_directives.new(**kwargs)

    def _fetch(self):
        messages = self.gmail.fetch(
            preferred_mime_type=self.args.mime_type,
            query=self.args.query,
            id_range=self.args.range)
        self.extract_directives.search_sources(
            *messages, stages='fetch')
        return messages

    def _send_requests(self, stage):
        if stage not in self.enabled_stages:
            return None, None

        sync_files = getattr(self.args, '{}_search'.format(stage))
        async_files = getattr(
            self.args, '{}_search_async'.format(stage))
        todo = sync_files or async_files
        assert todo
        logger.info('Sending {}-search requests'.format(stage))

        is_async = async_files is not None
        n = 0
        submit_requests = self._async_submit_requests if is_async \
            else self._sync_submit_requests
        succeeded = OrderedDict()
        failed = OrderedDict()

        while todo and n <= self.args.retry:
            n += 1
            curr_result = submit_requests(todo)
            todo = []

            for fname, resp in curr_result.items():
                if self._http_code_is_failure(resp.status_code):
                    todo.append(fname)
                    failed[fname] = resp
                    logger.error(
                        'Request {} failed with {}'.format(
                            fname, resp.status_code))
                else:
                    failed.pop(fname, None)
                    succeeded[fname] = resp
                    logger.info(
                        'Request {} succeeded with {}'.format(
                            fname, resp.status_code))

        self.extract_directives.search_sources(
            *succeeded.values(), stages=stage)
        return succeeded, failed

    def _sync_submit_requests(self, files):
        return {fname: self._send_request(fname)
                for fname in files}

    def _async_submit_requests(self, files):
        with ThreadPoolExecutor(
                max_workers=self.max_threads) as executor:
            futures = {
                executor.submit(self._send_request, fname
                                ): fname for fname in files}
            return {futures[f]: f.result()
                    for f in futures_as_completed(futures)}

    def _send_request(self, fname):
        logger.debug('Sending request in {}'.format(fname))
        with open(fname, 'rb') as fh:
            data = fh.read()
        # apply matches from all stages
        data = self.extract_directives.apply(data)

        kwargs = {}
        req_cls = HttpRequestRaw
        if not self.args.raw_socket:
            req_cls = HttpRequest
            kwargs['verify'] = self.args.verify_ssl
            kwargs['allow_redirects'] = self.args.allow_redirects
            if self.args.proxy:
                kwargs['proxies'] = {}
                kwargs['proxies']['http'] = \
                    kwargs['proxies']['https'] = \
                    'http://{}'.format(self.args.proxy)

        return req_cls(data,
                       timeout=self.args.timeout,
                       origin=self.args.origin,
                       is_ssl=self.args.is_ssl,
                       **kwargs).send()

    def _http_code_is_failure(self, status_code):
        def code_matches(codes):
            for code in codes:
                if re.match(str(code).replace('X', '[0-9]'),
                            str(status_code)):
                    return code

        if self.args.fail_codes is not None:
            return code_matches(self.args.fail_codes)
        return not code_matches(self.args.success_codes)

    def _print_line(self, fh, *cols):
        sep = ''
        for i, col in enumerate(cols):
            if i > 0:
                sep = '\t'
            fh.write('{}{}'.format(sep, col))
        fh.write('\n')

    def _print(self):
        if self.args.output is None:
            return

        with smart_open(self.args.output, 'a') as fh:
            self._print_line(fh, 'Name', 'Extracted value', 'Source')
            for ed in self.extract_directives:
                for i, ex in enumerate(ed.extracts, start=1):
                    self._print_line(
                        fh,
                        '{}_{}'.format(ed.name, i),
                        decode(ex.value),
                        ex.source)
