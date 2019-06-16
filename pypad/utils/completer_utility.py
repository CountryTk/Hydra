from nltk.tokenize import word_tokenize


def tokenize(file):
    classNames = []
    varNames = []
    functionNames = []
    ignore = ["(", ")", "[", "]", "{", "}", "#", "@", "!", "*"]
    try:
        with open(file, 'r') as openedFile:
            list = word_tokenize(openedFile.read())

        for index, names in enumerate(list):

            if list[index] == "def":
                if list[index + 1] not in functionNames:
                    functionNames.append(list[index + 1])

            if list[index] == "class":
                if list[index + 1] not in classNames:
                    classNames.append(list[index + 1])

            if list[index] == "=":
                if list[index - 1] not in classNames and list[index - 1] not in ignore:
                    varNames.append(list[index - 1])

        return classNames, varNames, functionNames

    except (FileNotFoundError, UnboundLocalError) as E:
        return "", "", ""


funcList = [
    "abs", "all", "any", "ascii", "bin", "bool", "breakpoint", "bytearray", "bytes", "callable",
    "chr", "classmethod",
    "compile", "complex",
    "delattr", "dict", "dir", "divmod", "enumerate", "eval", "exec", "filter", "float",
    "format",
    "frozenset",
    "getattr", "globals", "hasattr", "hash",
    "help", "hex", "id", "input", "int", "isinstance", "issubclass", "iter", "len", "list",
    "locals", "map",
    "max", "memoryview", "min", "next", "object",
    "oct", "open", "ord", "pow", "print", "property", "range", "repr", "reversed", "round",
    "set", "setattr", "slice", "sorted", "staticmethod", "str", "sum",
    "super", "tuple", "type", "vars", "zip", "__import__"
]

errorList = [

    'BaseException', 'Exception', 'ArithmeticError', 'BufferError',
    'LookupError', 'AssertionError', 'AttributeError', 'EOFError', 'FloatingPointError', 'GeneratorExit', 'ImportError',
    'ModuleNotFoundError', 'IndexError', 'KeyError', 'KeyboardInterrupt', 'MemoryError', 'NameError',
    'NotImplementedError', 'OSError', 'OverflowError', 'RecursionError', 'ReferenceError', 'RuntimeError',
    'StopIteration', 'StopAsyncIteration', 'SyntaxError', 'IndentationError', 'TabError', 'SystemError', 'SystemExit',
    'TypeError', 'UnboundLocalError', 'UnicodeError', 'UnicodeEncodeError', 'UnicodeDecodeError', 'ValueError',
    'ZeroDivisionError', 'EnvironmentError', 'IOError', 'WindowsError', 'BlockingIOError', 'ChildProcessError',
    'ConnectionError', 'BrokenPipeError', 'ConnectionAbortedError', 'ConnectionRefusedError', 'ConnectionResetError',
    'FileExistsError', 'FileNotFoundError', 'InterruptedError', 'IsADirectoryError', 'NotADirectoryError',
    'PermissionError', 'ProcessLookupError', 'TimeoutError', 'Warning', 'UserWarning', 'DeprecationWarning',
    'PendingDeprecationWarning', 'SyntaxWarning', 'RuntimeWarning', 'FutureWarning', 'ImportWarning', 'UnicodeWarning',
    'BytesWarning', 'ResourceWarning',

]

wordList = [
    # methods
    "abs(x)", "all(iterable)", "any(iterable)", "ascii(object)", "bin(x)", "bool([x])", "breakpoint(*args, **kwargs)",
    "bytearray([source[, encoding[, errors]]])", "bytes([source[, encoding[, errors]]])", "callable(object)",
    "chr(i)", "classmethod()",
    "compile(source, filename, mode, flags=0, dont_inherit=False, optimize=-1)", "complex([real[, imag]])",
    "delattr(object, name)", "dict(mapping, **kwarg)", "dir([object])", "divmod(a, b)", "enumerate(iterable, start=0)",
    "eval(expression, globals=None, locals=None)", "exec(object[, globals[, locals]])", "filter(function, iterable)",
    "float([x])", "format(value[, format_spec])", "frozenset([iterable])", "getattr(object, name[, default])",
    "globals()", "hasattr(object, name)", "hash(object)", "help([object])", "hex(x)", "id(object)", "input([prompt])",
    "int([x])", "isinstance(object, classinfo)", "issubclass(class, classinfo)", "iter(object[, sentinel])",
    "len(s)", "list([iterable])", "locals()", "map(function, variable)",
    "max(iterable, *[, key, default])", "memoryview(obj)", "min(iterable, *[, key, default])",
    "next(iterator[, default])", "object()",
    "oct(x)", "open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)",
    "ord(c)", "pow(x, y[, z])", "print(*objects, sep=' ', end='\\n', file=sys.stdout, flush=False)",
    "property(fget=None, fset=None, fdel=None, doc=None)", "range(stop)", "repr(object)", "reversed(seq)",
    "round(number[, ndigits])", "set([iterable])", "setattr(object, name, value)",
    "slice(start, stop[, step])", "sorted(iterable, *, key=None, reverse=False)", "staticmethod()",
    "str(object=b'', encoding='utf-8', errors='strict')", "sum(iterable[, start])",
    "super([type[, object-or-type]])", "tuple([iterable])", "type(name, bases, dict)", "vars([object])",
    "zip(*iterables)", " __import__(name, globals=None, locals=None, fromlist=(), level=0)¶",
    'False', 'None', 'True', 'and', 'as', 'assert', 'break', 'class',
    'continue', 'def', 'del', 'elif', 'else', 'except',
    'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise',
    'return', 'try',
    'while', 'with', 'yield', 'endswith()', '__name__',
    # warnings
    'BaseException', 'Exception', 'ArithmeticError', 'BufferError',
    'LookupError', 'AssertionError', 'AttributeError', 'EOFError', 'FloatingPointError', 'GeneratorExit', 'ImportError',
    'ModuleNotFoundError', 'IndexError', 'KeyError', 'KeyboardInterrupt', 'MemoryError', 'NameError',
    'NotImplementedError', 'OSError', 'OverflowError', 'RecursionError', 'ReferenceError', 'RuntimeError',
    'StopIteration', 'StopAsyncIteration', 'SyntaxError', 'IndentationError', 'TabError', 'SystemError', 'SystemExit',
    'TypeError', 'UnboundLocalError', 'UnicodeError', 'UnicodeEncodeError', 'UnicodeDecodeError', 'ValueError',
    'ZeroDivisionError', 'EnvironmentError', 'IOError', 'WindowsError', 'BlockingIOError', 'ChildProcessError',
    'ConnectionError', 'BrokenPipeError', 'ConnectionAbortedError', 'ConnectionRefusedError', 'ConnectionResetError',
    'FileExistsError', 'FileNotFoundError', 'InterruptedError', 'IsADirectoryError', 'NotADirectoryError',
    'PermissionError', 'ProcessLookupError', 'TimeoutError', 'Warning', 'UserWarning', 'DeprecationWarning',
    'PendingDeprecationWarning', 'SyntaxWarning', 'RuntimeWarning', 'FutureWarning', 'ImportWarning', 'UnicodeWarning',
    'BytesWarning', 'ResourceWarning',
    # built in modules
    'struct', 'string', 're', 'difflib', 'textwrap', 'unicodedata', 'stringprep',
    'readline', 'rlcompleter', 'codecs', 'datetime', 'calendar', 'collections', 'collections.abc', 'heapq', 'bisect'
                                                                                                            'array',
    'weakref', 'types', 'copy', 'pprint', 'reprlib', 'enum', 'numbers', 'math', 'cmath', 'decimal',
    'fractions', 'random', 'statistics', 'itertools', 'functools', 'operator', 'pathlib', 'os.path', 'fileinput',
    'stat', 'filecmp', 'tempfile', 'glob', 'fnmatch', 'linecache', 'shutil', 'macpath', 'pickle', 'copyreg', 'shelve',
    'marshal', 'dbm', 'sqlite3', 'zlib', 'gzip', 'bz2', 'lzma', 'zipfile', 'tarfile', 'csv', 'configparser', 'netrc',
    'xdrlib', 'plistlib', 'hashlib', 'hmac', 'secrets', 'os', 'io', 'time', 'argparse', 'getopt', 'logging',
    'logging.config', 'logging.handlers', 'getpass', 'curses', 'curses.textpad', 'curses.ascii', 'curses.panel',
    'platform',
    'errno', 'ctypes', 'threading', 'multiprocessing', 'concurrent', 'subprocess', 'sched', 'queue', '_thread',
    '_dummy_thread',
    '_dummy_threading', 'asyncio', 'socket', 'ssl', 'select', 'selectors', 'asyncore', 'asynchat', 'signal', 'mmap',
    'email',
    'json', 'mailcap', 'mailbox', 'mimetypes', 'base64', 'binhex', 'binascii', 'quopri', 'uu', 'html', 'html.parser',
    'html.entities', 'xml', 'webbrowser', 'cgi', 'cgitb', 'wsgiref', 'urllib', 'urllib.request', 'urllib.response',
    'urllib.parse', 'urllib.error', 'http', 'http.client', 'ftplib', 'poplib', 'imaplib', 'nntplib', 'smtplib',
    'smtpd', 'telnetlib', 'uuid', 'socketserver', 'http.server', 'http.cookies', 'http.cookiejar', 'xmlrpc',
    'ipaddress',
    'audioop', 'aifc', 'sunau', 'wave', 'chunk', 'colorsys', 'imghdr', 'sndhdr', 'ossaudiodev', 'gettext', 'locale',
    'turtle', 'cmd',
    'shlex', 'tkinter', 'tkinter.ttk', 'tkinter.tik', 'tkinter.scrolledtext', 'typing', 'pydoc', 'doctest', 'unittest',
    'unittest.mock',
    '2to3', 'test', 'test.support', 'bdb', 'faulthandler', 'pdb', 'timeit', 'trace', 'tracemalloc' 'distutils',
    'ensurepip', 'venv',
    'zipapp', 'sys', 'sysconfig', 'builtins', '__main__', 'warnings', 'dataclasses', 'contextlib', 'abc', 'textit',
    'traceback',
    '__future__', 'gc', 'inspect', 'site', 'code', 'codeop', 'zipimport', 'pkgutil', 'modulefinder', 'runpy',
    'importlib', 'parser',
    'ast', 'symtable', 'symbol', 'token', 'keyword', 'tokenize', 'tabnanny', 'pyclbr', 'py_compile', 'compileall',
    'dis',
    'pickletools', 'formatter', 'msilib', 'msvcrt', 'winreg', 'winsound', 'posix', 'pwd', 'spwd', 'grp', 'crypt',
    'termios',
    'tty', 'pty', 'fcntl', 'pipes', 'resource', 'nis', 'syslog', 'optparse', 'imp'
]
wordList = sorted(wordList)
