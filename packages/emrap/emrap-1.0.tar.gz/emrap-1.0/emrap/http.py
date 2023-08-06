import logging
import socket
import requests
import ssl
import re
from datetime import datetime
from time import time
from contextlib import contextmanager
try:
    from http_parser.parser import HttpParser
except ImportError:
    from http_parser.pyparser import HttpParser
from http_parser.http import HttpStream
from http_parser.reader import SocketReader

from .utils import str_trunc, smart_open
from .common import Searchable
from .extracts import OrderedExtracts


logger = logging.getLogger(__name__)


class ParseError(RuntimeError):
    pass

class _BaseHttp(Searchable):
    _type = None
    _extract_type = OrderedExtracts

    def __init__(self, source):
        '''
        source: one of:
            - binary data, the raw HTTP request/response
            - a socket object to read from
            - a string filename to read from
            - a file-like object open for binary reading
            - open file descriptor (integer)
        '''

        super().__init__()
        self.timestamp = None
        self._parser = None
        self.raw = self._parse(source)
        self.headers = self._parser.get_headers()
        self.content = self._parser.recv_body()
        assert int(self.headers['Content-Length']) == \
            len(self.content)

    @property
    def time(self):
        if self.timestamp is None:
            return None
        return datetime.fromtimestamp(
            self.timestamp).strftime('%d %b %Y %H:%M:%S')

    @property
    def raw_headers(self, headers=None):
        '''Headers as a single multi-line UTF-8 string'''

        return '\r\n'.join(
            ': '.join([hdr, val])
            for hdr, val in self.headers.items()).encode('utf-8')

    @property
    def content(self):
        '''Raw body as a bytes string'''

        return self._content

    @content.setter
    def content(self, content):
        '''Updates Content-Length'''

        self._content = content
        self.headers['Content-Length'] = str(len(content))

    @property
    def text(self):
        '''Decoded body as a string'''

        return self.content.decode('utf-8', errors='replace')

    def search(self, regex,
               where=['raw_headers', 'content'], **kwargs):
        '''Search within the body and/or headers for the given regex

        See Searchable._search for description of the arguments
        '''

        return self._search(regex, where=where, **kwargs)

    def _parse(self, source, retry=True):
        self._parser = HttpParser()

        if isinstance(source, bytes):
            parse = self._parse_from_data
        elif isinstance(source, socket.socket):
            parse = self._parse_from_sock
        else:
            parse = self._parse_from_file

        raw, raw_parsed = parse(source)
        ninput = len(raw)
        nread = len(raw_parsed)
        if nread != ninput:
            # when this happens, the parser returns DELETE for method,
            # not sure if a bug or intentional; so we need to parse it
            # again with the truncated data
            msg = ('Read {} bytes from {} data, expected {}. '
                   'Check you Content-Length header').format(
                       nread, self._type, ninput)
            if retry:
                logger.warning(msg)
                self._parse(raw_parsed, retry=False)
                return raw
            raise ParseError(msg)

        if not self._parser.is_headers_complete():
            logger.warning(
                'Got incomplete {} headers'.format(self._type))
        if not self._parser.is_message_complete():
            logger.warning(
                'Got incomplete {} body'.format(self._type))
        assert len(raw) == len(raw_parsed)
        return raw

    def _parse_from_data(self, data):
        nread = self._parser.execute(data, len(data))
        return data, data[:nread]

    def _parse_from_sock(self, sock):
        raw_parsed = raw = b''
        while True:
            data = sock.recv(1024)
            if not data:
                break
            raw += data
            raw_parsed += self._parse_from_data(data)[1]
            if self._parser.is_message_complete():
                break
        return raw, raw_parsed

    def _parse_from_file(self, file_or_fd):
        with smart_open(file_or_fd, 'rb') as fh:
            data = fh.read()
        return data, self._parse_from_data(data)

    def __repr__(self):
        return '{type}({time})'.format(
            type=self.__class__.__name__,
            time=self.time)

    def __str__(self):
        return self.__repr__()

class _BaseHttpRequest(_BaseHttp):
    _type = 'request'
    _default_ports = {'https:': 443, 'http:': 80}

    def __init__(self, source, /,
                 timeout=None, origin=None, is_ssl=None, **kwargs):
        '''
        origin is of the form protocol//host[:port]
        '''

        super().__init__(source, **kwargs)
        if None not in [origin, is_ssl]:
            raise TypeError(
                'Only one of origin or is_ssl '
                'can be given')

        self._timeout = timeout
        # the below are set/overriden by origin
        self._protocol = None
        if is_ssl is not None:
            # explicitly given
            self._protocol = 'https:' if is_ssl else 'http:'
        self._hostname = None
        self._port = None

        if origin is None:
            try:
                origin = '{}//{}'.format(
                    '' if self._protocol is None else self._protocol,
                    self.headers['Host'])
            except KeyError:
                raise ValueError(
                    'Neither Host header nor origin given')
        self.origin = origin

        self.method = self._parser.get_method()
        self.pathname = self._parser.get_path()
        self.search = self._parser.get_query_string()
        self.hash = self._parser.get_fragment()

    @property
    def protocol(self):
        '''http: or https:'''
        return self._protocol

    @property
    def hostname(self):
        return self._hostname

    @property
    def port(self):
        if self._port is None:
            return self._default_ports[self.protocol]
        return self._port

    @property
    def host(self):
        '''Hostname[:port]'''
        suffix = ''
        if self._port is not None:
            suffix = ':{}'.format(self.port)
        return '{}{}'.format(self.hostname, suffix)

    @property
    def base_href(self):
        '''Full path including query and hash'''
        # don't use parser.get_url() since changes to pathname, search
        # or hash won't be reflected
        base_href = self.pathname
        if self.search:
            base_href += '?{}'.format(self.search)
        if self.hash:
            base_href += '#{}'.format(self.hash)
        return base_href

    @property
    def href(self):
        '''Full URL incuding origin'''
        return '{}{}'.format(self.origin, self.base_href)

    @property
    def url(self):
        '''alias for href'''
        return self.href

    @property
    def is_ssl(self):
        return self.protocol == 'https:'

    @property
    def origin(self):
        '''protocol//host[:port]'''
        return self._origin

    @origin.setter
    def origin(self, origin):
        origin = origin.rstrip('/')

        match = re.match(
            '(?P<protocol>https?:)?//'
            '(?P<hostname>[\w.-]+)'
            '(:(?P<port>[0-9]+))?$',
            origin, flags=re.I)
        if not match:
            raise ValueError(
                "Can't parse {} as an origin".format(origin))

        hostname = match['hostname']
        port = match['port']
        if port is not None:
            try:
                port = int(port)
            except ValueError:
                raise ValueError(
                    "Can't parse {} as an origin".format(origin))

        protocol = match['protocol']
        if protocol is None:
            protocol = \
                'https:' if str(port).endswith('443') else 'http:'

        self._hostname = hostname
        self._port = port
        self._protocol = protocol
        self._origin = '{}//{}'.format(self.protocol, self.host)

    def __repr__(self):
        return '{type}({url}, {time})'.format(
            type=self.__class__.__name__,
            url=self.href,
            time=self.time)

class HttpRequestRaw(_BaseHttpRequest):
    '''Sends the given data as is

    In case the Content-Length header did not reflect the length of
    the body, then looking up Content-Length via the headers
    dictionary or viewing the body via content won't match the request
    that will be sent (the original data).
    '''

    def send(self):
        '''Replacements match anywhere in the raw HTTP request'''

        logger.debug('Sending raw request to {}:{}'.format(
            self.hostname, self.port))
        logger.trace(str_trunc(self.raw, 200))

        self.timestamp = time()
        with self._socket() as sock:
            sock.send(self.raw)
            resp = HttpResponse(sock, url=self.url)

        logger.debug('Got {}'.format(resp.status_code))
        logger.trace('Headers:\n{}'.format(resp.headers))
        logger.trace('Body:\n{}'.format(str_trunc(resp.content, 100)))
        return resp

    @contextmanager
    def _socket(self):
        '''Yields either a plain or SSL socket'''

        sock = plain_sock = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        ssl_sock = None
        if self.is_ssl:
            sock = ssl_sock = ssl.wrap_socket(plain_sock)
        sock.settimeout(self._timeout)
        try:
            sock.connect((self.hostname, self.port))
            yield sock
        finally:
            plain_sock.close()
            if ssl_sock is not None:
                ssl_sock.shutdown(socket.SHUT_RDWR)
                ssl_sock.close()

class HttpRequest(_BaseHttpRequest):
    '''Uses the requests package

    requests does processing, including:
     - location hash will be removed
     - Content-Length will be updated
     - Host, User-Agent, Accept-Encoding will be added if not present

    Header order will be preserved
    '''

    def __init__(self,
                 *args,
                 verify=True,
                 proxies=None,
                 allow_redirects=True,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.verify = verify
        self.proxies = proxies
        self.allow_redirects = allow_redirects
        self._session = requests.Session()
        # Use a session since passing headers as a kwarg to request
        # does not preserve header order
        self._session.headers = self.headers

    def send(self):
        '''Replacements match in URL, headers and body'''

        logger.debug('Sending {} {}'.format(self.method, self.href))
        logger.trace(str_trunc(self.headers, 100))
        logger.trace(str_trunc(self.content, 100))

        self.timestamp = time()
        resp = self._session.request(
            self.method,
            self.href,
            data=self.content,
            verify=self.verify,
            proxies=self.proxies,
            allow_redirects=self.allow_redirects,
            timeout=self._timeout)
        logger.debug('Got {}'.format(resp.status_code))
        logger.trace('Headers:\n{}'.format(resp.headers))
        logger.trace('Body:\n{}'.format(str_trunc(resp.content, 100)))

        # Reconstruct the raw HTTP request; TODO is there a way to get
        # it from the urllib3.Response object??
        # response has already been decoded and assembled if needed
        headers = resp.headers.copy()
        headers.pop('Transfer-Encoding', None)
        headers.pop('Content-Encoding', None)
        headers['Content-Length'] = str(len(resp.content))

        raw_status_line = 'HTTP/{version:.1f} {code} {reason}'.format(
            version=resp.raw.version / 10,
            code=resp.status_code,
            reason=resp.reason).encode('utf-8')
        raw_headers = '\r\n'.join(
            ': '.join([hdr, val])
            for hdr, val in headers.items()).encode('latin1')
        raw_data = b'\r\n'.join([
            raw_status_line,
            raw_headers,
            b'',
            resp.content])
        return HttpResponse(raw_data, url=self.url)

class HttpResponse(_BaseHttp):
    _type = 'response'

    def __init__(self, *args, url=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.timestamp = time()
        self.url = url
        self.status_code = self._parser.get_status_code()

    def __repr__(self):
        return '{type}({url} -> {code}, {time}'.format(
            type=self.__class__.__name__,
            url=self.url or 'unknown',
            code=self.status_code,
            time=self.time)
