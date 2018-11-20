import glob
import socket
import uuid

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

BUFSIZE = 1024
SUPPORTED_LANGUAGES = (
    'c',
    'cc',
    'java',
    'ml',
    'pascal',
    'ada',
    'lisp',
    'scheme',
    'haskell',
    'fortran',
    'ascii',
    'vhdl',
    'perl',
    'matlab',
    'python',
    'mips',
    'prolog',
    'spice',
    'vb',
    'csharp',
    'modula2',
    'a8086',
    'javascript',
    'plsql',
    'verilog')

for lang in SUPPORTED_LANGUAGES:
    globals()['MOSS_LANG_%s' % lang.upper()] = lang


class MOSSException(Exception):
    pass


class MOSS(object):
    def __init__(self, user_id, language,
                 moss_host='moss.stanford.edu',
                 moss_port=7690,
                 sensitivity=10,  # -m
                 comment='',  # -c
                 matching_file_limit=250,  # -n
                 use_experimental_server=False,  # -x
                 directory=False):
        if language not in SUPPORTED_LANGUAGES:
            raise ValueError(
                "language '%s' not in %s" % (language, SUPPORTED_LANGUAGES))

        self.user_id = user_id
        self.language = language
        self.moss_host = moss_host
        self.moss_port = moss_port
        self.sensitivity = sensitivity
        self.comment = comment
        self.matching_file_limit = matching_file_limit
        self.use_experimental_server = use_experimental_server
        self.directory = directory
        self.staged_files = [[], []]

    def add_file_from_disk(self, path, wildcard=False, display_name=None,
                           **kwargs):
        if wildcard and display_name:
            raise ValueError(
                'wildcard mode incompatible with display_name')

        files = glob.glob(path) if wildcard else [path]
        for path in files:
            with open(path, 'r') as f:
                self.add_file_from_memory(path, f.read(),
                                          display_name=display_name, **kwargs)

    def add_file_from_memory(self, virtual_path, content,
                             base=False, display_name=None):
        if display_name is None:
            display_name = virtual_path.replace(' ', '_')

        self.staged_files[base].append((virtual_path, content, display_name))

    def _url_is_valid(self, url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc, result.path])
        except:
            return False

    def _process_file(self, sock, file_id, path, content, display_name):
        sock.sendall('file %d %s %s %s\n' % (file_id, self.language,
                                          len(content), display_name))
        sock.sendall(content)

    def process(self):
        sock = socket.socket()
        sock.connect((self.moss_host, self.moss_port))
        sock.sendall('moss %d\n' % self.user_id)
        sock.sendall('directory %s\n' % int(self.directory))
        sock.sendall('X %d\n' % int(self.use_experimental_server))
        sock.sendall('maxmatches %d\n' % self.sensitivity)
        sock.sendall('show %d\n' % self.matching_file_limit)
        sock.sendall('language %s\n' % self.language)

        resp = sock.recv(BUFSIZE)
        if resp.strip() == 'no':
            raise MOSSException(
                    "language '%s' not accepted by server" % self.language)

        for path, content, name in self.staged_files[1]:
            self._process_file(sock, 0, path, content, name)

        for i, (path, content, name) in enumerate(self.staged_files[0]):
            self._process_file(sock, i + 1, path, content, name)

        sock.sendall('query 0 %s\n' % self.comment)

        resp = sock.recv(BUFSIZE)
        sock.sendall('end\n')
        sock.close()

        url = resp.strip()
        if not self._url_is_valid(url):
            raise MOSSException(
                    "server returned invalid response URL '%s'" % url)

        return url

