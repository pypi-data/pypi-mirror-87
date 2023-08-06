import re
import sys
import string
import random
from collections.abc import Iterable, Mapping
from collections import UserDict
from contextlib import contextmanager


def str_remove_chars(s, skip):
    return s.translate(str.maketrans(dict.fromkeys(skip)))

def randstr(size,
            use_lower=True,
            use_upper=True,
            use_digit=True,
            use_punct=False,
            skip=''):
    '''Returns a random string of length size

    The string consists of letters, digits and punctuation excluding
    any characters given in skip.
    '''

    alphabet = ''
    if use_lower:
        alphabet += string.ascii_lowercase
    if use_upper:
        alphabet += string.ascii_uppercase
    if use_digit:
        alphabet += string.digits
    if use_punct:
        alphabet += string.punctuation
    if skip:
        alphabet = str_remove_chars(alphabet, skip)
    return ''.join([random.choice(alphabet) for i in range(size)])

def is_seq_like(val):
    '''True if val is an iterable (but not a string, or dict)

    i.e. if it's a list, set, tuple, or some mutable sequence
    '''

    return isinstance(val, Iterable) \
        and not isinstance(val, (str, bytes, Mapping))

def nat(s):
    '''Converts string to a natural number (non-negative integer)'''

    n = int(s)
    if n < 0:
        raise ValueError(
            '{} is an invalid positive int value'.format(s))
    return n

def str_trunc(s, size):
    '''Truncates string or bytes to length size, appending ...'''

    if len(s) <= size:
        return s
    if isinstance(s, bytes):
        suff = b'...'
    else:
        suff = '...'
    return s[:size - 3] + suff

def str_to_re_flags(flags):
    '''Converts a string of letters to bitwise-OR'd regex flags'''

    if isinstance(flags, int):
        return flags
    regex_flags = 0
    for f in flags:
        regex_flags |= getattr(re, f.upper())
    return regex_flags

@contextmanager
def smart_open(arg, *args, **kwargs):
    '''Returns a file-like object

    arg: one of
        - string filename
        - file-like-object
        - open file descriptor (integer)
        - "-" for stdout
    '''

    # close it only if it was a filename, but not if it was an
    # opened FD or file-like object
    do_close = isinstance(arg, str)
    try:
        if arg == '-':
            fh = sys.stdout
        elif isinstance(arg, (str, int)):
            fh = open(arg, *args, **kwargs)
        elif hasattr(arg, 'read'):
            fh = arg
        else:
            raise TypeError("Can't parse data from <{}>".format(
                arg.__class__.__name__))
        yield fh
    finally:
        if do_close:
            fh.close()

def encode(v, encoding='utf-8'):
    '''Encodes string in encoding if not already bytes'''

    if isinstance(v, bytes):
        return v
    return v.encode(encoding)

def decode(v, encoding='utf-8'):
    '''Decodes string in encoding if not already str'''

    if isinstance(v, str):
        return v
    return v.decode(encoding)

def decode_or_encode(v, ref, encoding='utf-8'):
    '''Decodes or encodes string in encoding to match type of ref

    ref is a str or bytes
    '''

    if isinstance(ref, str):
        return decode(v, encoding=encoding)
    return encode(v, encoding=encoding)
