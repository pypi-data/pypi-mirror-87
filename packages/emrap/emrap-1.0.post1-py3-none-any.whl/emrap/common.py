import logging
import re
from collections.abc import Sequence
from time import time
import bisect

from .utils import str_to_re_flags, decode_or_encode


logger = logging.getLogger(__name__)


class Searchable:
    _extract_type = None

    def __init__(self):
        super().__init__()
        if self._extract_type is None:
            raise NotImplementedError('This is an abstract class')

    def search(self, regex, **kwargs):
        return self._search(regex, **kwargs)

    def _search(self,
                regex,
                regex_group=0,
                regex_flags='',
                where=[],
                skip_missing_attr=False):
        '''
        - regex is the pattern to search. Its type will match each
          item to be compared, so it doesn't matter if it's a str or
          bytes
        - regex_flags can be a string of letters corresponding to the
          short flag names in re, or an integer in which case it's
          passed to re.search as is
        - regex_group selects which capture group from the regex to
          take
        - where specifies whether to search in content,
          raw_headers or both
        - skip_missing_attr: do not error if any of the given
          attributes in where are not found
        '''

        def find(in_attr):
            try:
                data = getattr(self, in_attr)
            except AttributeError:
                if skip_missing_attr:
                    logger.trace('Skipping {}'.format(in_attr))
                    return []
                raise

            values = []
            for m in re.finditer(decode_or_encode(regex, data), data):
                values.append(m.group(regex_group))
            logger.trace('Matched in {}: {}'.format(in_attr, values))

            return values

        flags = str_to_re_flags(regex_flags)
        logger.trace('Using regex {} wih flags {!r}'.format(
            regex, flags))

        logger.debug('Searching {} for {} in {}'.format(
            self, regex, where))
        # if class is cacheable, then check cache
        if isinstance(self, Cacheable):
            self._last_cache_key = cache_key = \
                (regex, regex_group, flags, ','.join(sorted(where)))
            try:
                logger.trace('[From cache] {} -> {}'.format(
                    regex, self[cache_key]))
                return self[cache_key]
            except KeyError:
                self.new_cache(cache_key)

        extracts = self._extract_type()
        # search separately in each section rather than concatenating
        # them, since if re.MULTILINE is not in the flags, then
        # ^ would only match at the beginning of the text
        for in_attr in where:
            for v in find(in_attr):
                extracts.new(value=v, source=self)

        if isinstance(self, Cacheable):
            # save cache
            for e in extracts:
                self.add_cache_item(cache_key, e)

        logger.trace('[Fresh search] {} -> {}'.format(
            regex, extracts))
        return extracts

class Sortable:
    @property
    def _comparables(self):
        '''Should return a value that is used for comparison'''
        raise NotImplementedError

    def __ensure_implemented(self, other):
        if not isinstance(other, Sortable):
            raise TypeError(
                "Cannot compare '{}' to '{}'".format(
                    self.__class__.__name__,
                    other.__class__.__name__))

    def __eq__(self, other):
        return isinstance(other, Sortable) and \
            self._comparables == other._comparables

    def __ne__(self, other):
        return isinstance(other, Sortable) and \
            self._comparables != other._comparables

    def __lt__(self, other):
        self.__ensure_implemented(other)
        return self._comparables < other._comparables

    def __le__(self, other):
        self.__ensure_implemented(other)
        return self._comparables <= other._comparables

    def __gt__(self, other):
        self.__ensure_implemented(other)
        return self._comparables > other._comparables

    def __ge__(self, other):
        self.__ensure_implemented(other)
        return self._comparables >= other._comparables

class Cacheable:
    '''Supports iteration, the in operator and getting items via []'''

    _holds = None

    def __init__(self):
        super().__init__()
        self._search_cache = {}
        if self._holds is None:
            raise NotImplementedError('This is an abstract class')

    def new_cache(self, cache_key, *args, **kwargs):
        '''Creates a new cache holding a type self._holds

        Any given arguments are passed to the constructor of
        self._cahces.
        Returns a tuple of the new item and the timestamp.
        '''

        self.__ensure_not_exists(cache_key)
        return self._reset_cache(cache_key, *args, **kwargs)

    def reset_cache(self, cache_key, *args, **kwargs):
        '''Resets the store with the given cache key'''

        self.__ensure_exists(cache_key)
        return self._reset_cache(cache_key, *args, **kwargs)

    def new_cache_item(self, cache_key, *args, **kwargs):
        '''Creates a new item and adds it to the store with the given
        cache key.

        self._holds must implement the new method
        Returns the timestamp.
        '''

        self.__ensure_exists(cache_key)
        return self._new_cache_item(cache_key, *args, **kwargs)

    def add_cache_item(self, cache_key, *args, **kwargs):
        '''Adds an item to the store with the given cache key

        Returns the timestamp.
        '''

        self.__ensure_exists(cache_key)
        return self._add_cache_item(cache_key, *args, **kwargs)

    def last_modified(self, cache_key):
        '''Returns the timestamp for the given cache key'''

        self.__ensure_exists(cache_key)
        return self._search_cache[cache_key]['last_modified']

    def _new_cache_item(self, cache_key, *args, **kwargs):
        '''This assumes the store has a new method'''

        cache = self._search_cache[cache_key]
        if hasattr(cache['store'], 'new'):
            cache['store'].new(*args, **kwargs)
        else:
            raise TypeError(
                'Cannot add an item to type {}'.format(
                    cache['store'].__class__.__name__))
        return self.__touch(cache_key)

    def _add_cache_item(self, cache_key, item):
        '''This assumes the store is a sequence

        Child class overrides if needed'''

        cache = self._search_cache[cache_key]
        if hasattr(cache['store'], 'add'):
            cache['store'].add(item)
        elif hasattr(cache['store'], 'append'):
            cache['store'].append(item)
        elif hasattr(cache['store'], 'extend'):
            cache['store'].extend([item])
        elif hasattr(cache['store'], '__add__'):
            cache['store'] += [item]
        else:
            raise TypeError(
                'Cannot add an item to type {}'.format(
                    cache['store'].__class__.__name__))
        return self.__touch(cache_key)

    def _reset_cache(self, cache_key, *args, **kwargs):
        '''Creates a new cache holding a type self._holds

        Any given arguments are passed to the constructor of
        self._cahces
        '''

        self._search_cache[cache_key] = {}
        self._search_cache[cache_key]['store'] = \
            self._holds(*args, **kwargs)
        return self.__touch(cache_key)

    def __ensure_not_exists(self, cache_key):
        if cache_key in self._search_cache:
            raise KeyError(
                '{} already in store, reset it first'.format(
                    cache_key))

    def __ensure_exists(self, cache_key):
        if cache_key not in self._search_cache:
            raise KeyError(
                '{} not in store, create it first'.format(
                    cache_key))

    def __touch(self, cache_key):
        ts = time()
        self._search_cache[cache_key]['last_modified'] = ts
        return ts

    def __contains__(self, cache_key):
        return cache_key in self._search_cache

    def __iter__(self):
        return iter(self._search_cache)

    def __str__(self):
        return str(self._search_cache)

    def __repr__(self):
        return repr(self._search_cache)

    def __len__(self):
        return len(self._search_cache)

    def __getitem__(self, cache_key):
        return self._search_cache[cache_key]['store']

class Container(Sequence):
    # mostly copy-paste from collections.UserList
    '''A list-like class which has a defined order of insertion

    It does not implement an insert or append method, instead it
    implements an add method which inserts the item in the correct
    place.

    This base class does not set an order. Child classes must
    implement the _add_item method, which is the only method that
    modifies the data. The _item_is_accepted method decides if the
    item is to be added. Thus the order of insertion is implemented in
    _add_item and filtering of items (such as rejecting duplicates)
    should be done in _item_is_accepted. The only method that calls
    _add_item is _add_items and that can be overridden in order to
    change the order in which a list of items is added.
    '''
    _holds = None

    def __init__(self, initlist=[]):
        super().__init__()
        if self._holds is None:
            raise NotImplementedError('This is an abstract class')
        self._data = []
        self += initlist

    def add(self, item):
        if not isinstance(item, self._holds):
            raise TypeError('item must be a {}'.format(
                self._holds.__class__.__name__))
        self += [item]

    def new(self, *args, **kwargs):
        '''Create a new item and add it to the collection

        Returns the item
        '''

        item = self._holds(*args, **kwargs)
        self.add(item)
        return item

    def pop(self, i=-1):
        return self._data.pop(i)

    def remove(self, item):
        self._data.remove(item)

    def clear(self):
        self._data.clear()

    def copy(self):
        return self.__class__(self)

    def count(self, item):
        return self._data.count(item)

    def index(self, item, *args):
        return self._data.index(item, *args)

    def extend(self, other):
        self += other

    def _add_item(self, item):
        raise NotImplementedError('This is an abstract method')

    def _add_items(self, items):
        for item in items:
            if self._item_is_accepted(item):
                self._add_item(item)

    def _item_is_accepted(self, item):
        return True

    def __repr__(self):
        return repr(self._data)

    def __lt__(self, other):
        return self._data < self.__cast(other)

    def __le__(self, other):
        return self._data <= self.__cast(other)

    def __eq__(self, other):
        return self._data == self.__cast(other)

    def __gt__(self, other):
        return self._data > self.__cast(other)

    def __ge__(self, other):
        return self._data >= self.__cast(other)

    def __cast(self, other):
        return other._data if isinstance(
            other, Container) else other

    def __contains__(self, item):
        return item in self._data

    def __len__(self):
        return len(self._data)

    def __getitem__(self, i):
        if isinstance(i, slice):
            return self.__class__(self._data[i])
        else:
            return self._data[i]

    #  def __setitem__(self, i, item):
    #      raise NotImplementedError

    def __delitem__(self, i):
        del self._data[i]

    def __add__(self, other):
        if isinstance(other, Container):
            return self.__class__(self._data + other._data)
        elif isinstance(other, type(self._data)):
            return self.__class__(self._data + other)
        return self.__class__(self._data + list(other))

    def __radd__(self, other):
        if isinstance(other, Container):
            return self.__class__(other._data + self._data)
        elif isinstance(other, type(self._data)):
            return self.__class__(other + self._data)
        return self.__class__(list(other) + self._data)

    def __iadd__(self, other):
        if isinstance(other, SortedContainer):
            toadd = other._data
        elif isinstance(other, type(self._data)):
            toadd = other
        else:
            toadd = list(other)

        self._add_items(toadd)
        return self

    def __mul__(self, n):
        return self.__class__(self.data * n)

    __rmul__ = __mul__

    def __imul__(self, n):
        self._data *= n
        return self

    def __copy__(self):
        inst = self.__class__.__new__(self.__class__)
        inst.__dict__.update(self.__dict__)
        # Create a copy and avoid triggering descriptors
        inst.__dict__['data'] = self.__dict__['data'][:]
        return inst

class UniqueContainer(Container):
    def _item_is_accepted(self, item):
        return item not in self._data

class OrderedContainer(Container):
    '''Stores items in the order they were added with newer ones at
    the end'''

    def _add_item(self, item):
        self._data.append(item)

class ReverseOrderedContainer(Container):
    '''Stores items in the order they were added with newer ones at
    the front

    If multiple items are added at once, such as with extend, their
    order is preserved but they are inserted at the front
    '''

    def _add_items(self, items):
        # do not reverse order
        super()._add_items(items[::-1])

    def _add_item(self, item):
        self._data.insert(0, item)

class OrderedUniqueContainer(OrderedContainer, UniqueContainer):
    '''Stores unique items in the order they were added with newer
    ones at the end

    Duplicate items are moved to the end.
    '''

    def _add_items(self, items):
        # remove existing ones so they can be added in the correct
        # position
        for item in items:
            if item in self:
                self.remove(item)
        super()._add_items(items)

class ReverseOrderedUniqueContainer(
        ReverseOrderedContainer, OrderedUniqueContainer):
    '''Stores unique items in the order they were added with newer
    ones at the front

    Duplicate items are moved to the front.
    '''

    pass

class SortedContainer(Container):
    '''Stores items in ascending sorted order'''

    def _add_item(self, item):
        bisect.insort(self._data, item)

class SortedUniqueContainer(SortedContainer, UniqueContainer):
    '''Stores unique items in ascending sorted order'''

    pass
