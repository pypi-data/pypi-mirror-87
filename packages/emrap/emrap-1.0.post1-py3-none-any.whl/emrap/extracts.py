import logging
import re
from functools import partial
from copy import deepcopy

from .common import Searchable, Sortable, Container, \
    OrderedContainer, ReverseOrderedContainer, \
    OrderedUniqueContainer, ReverseOrderedUniqueContainer, \
    SortedContainer, SortedUniqueContainer
from .utils import nat, is_seq_like, decode_or_encode


logger = logging.getLogger(__name__)


class Extract(Sortable):
    '''Comparison operates on the timestamp, then value'''

    def __init__(self, value, source):
        super().__init__()
        if None in [value, source]:
            raise TypeError('value and source must be non-null')
        self.value = value
        self.source = source

    @property
    def _comparables(self):
        return (self.source, self.value)

    def __repr__(self):
        return '{}({!r}, {!r})'.format(
            self.__class__.__name__, self.value, self.source)

    def __str__(self):
        return self.__repr__()

class _BaseExtracts(Container):
    _holds = Extract

    def get(self, value=None, **source_kwargs):
        def matches_source(attr, val):
            source_val = getattr(self.source, attr)
            if isinstance(val, tuple):
                if len(val) != 2:
                    raise TypeError(
                        '{} value has to be a single item or '
                        'a two-item tuple')
                return source_val >= val[0] and source_val <= val[1]
            return source_val == val

        result = self.__class__()
        for e in self:
            if value not in [None, e.value]:
                continue
            match = True
            for attr, val in source_kwargs.items():
                if not matches_source(attr, val):
                    match = False
                    break
            if match:
                result.add(e)
        return result

class OrderedExtracts(_BaseExtracts, OrderedContainer):
    pass

class ReverseOrderedExtracts(_BaseExtracts, ReverseOrderedContainer):
    pass

class OrderedUniqueExtracts(_BaseExtracts, OrderedUniqueContainer):
    pass

class ReverseOrderedUniqueExtracts(
        _BaseExtracts, ReverseOrderedUniqueContainer):
    pass

class SortedExtracts(_BaseExtracts, SortedContainer):
    pass

class SortedUniqueExtracts(_BaseExtracts, SortedUniqueContainer):
    pass

class ExtractDirectives:
    '''A class to store search directives which can be applied to
    Searchable sources. Found matches can replace placeholders in
    given data.

    Implemented directives can be accessed either as items via [] or
    as attributes.
    '''

    _implements = [
        # this gives all allowed items
        'name',
        'stages',
        'where',
        'regex',
        'regex_group',
        'regex_flags',
        'default'
    ]

    _defaults = {
        # if there are no defaults, then it is required
        'stages': None,
        'regex_group': 0,
        'regex_flags': '',
        'default': 'NOT FOUND',
    }

    _conversions = {
        'name': str,
        'stages': partial(re.split, ' *, *'),
        'where': partial(re.split, ' *, *'),
        'regex_group': nat,
        'default': str
    }

    _type_constraints = {
        'regex': (str, bytes, re.Pattern),
        'regex_flags': (int, str),
    }

    _value_constraints = {
        # if the value to be compared is a list, then it's required to
        # be a subset of the given list; otherwise to be one of the
        # items in the list, e.g.
        # 'stages': ['stage1', 'stage2']
        # will allow stages to be either of the above two, or a list
        # of both
    }

    def __init__(self, left='{%', right='%}', **directives):
        '''Parses a list of directives

        left and right determine how to find the replacement point
        when applying to text: will match {left}{name}{right}, e.g.
        {%injection_point%}
        '''

        super().__init__()
        self._directives = deepcopy(self._defaults)
        self._left = left
        self._right = right
        self._extracts = ReverseOrderedUniqueExtracts()
        for key, val in directives.items():
            self[key] = val

        for key in self._implements:
            if key not in self:
                raise ValueError('{} is required'.format(key))

    @property
    def extracts(self):
        return self._extracts

    @property
    def search_kwargs(self):
        return {'regex': self.regex,
                'regex_group': self.regex_group,
                'regex_flags': self.regex_flags,
                'where': self.where}

    def search_sources(self, *sources):
        '''Searches sources and saves found extracts

        Sources are in order of precedence, i.e. matches from the
        first one will be replaced first.

        Returns the found extracts.
        '''

        extracts = self.extracts.__class__()
        for s in sources[::-1]:
            extracts.extend(s.search(**self.search_kwargs,
                                     skip_missing_attr=True))
        self.extracts.extend(extracts)
        return extracts

    def get_placeholder(self, i=None, escape=False):
        suff = ''
        if i == '*':
            suff = '(_[0-9]+)?'  # regex
        elif i is not None:
            suff = '_{}'.format(i)

        placeholder = '{left}{name}{suff}{right}'.format(
            left=self._left,
            name=self.name,
            suff=suff,
            right=self._right)
        if escape:
            placeholder.replace('%', '%%')
            placeholder.replace('{', '{{')
            placeholder.replace('}', '}}')
        return placeholder

    def apply(self, target, *sources, only_found=False):
        '''Applies the replacements found so far to target text

        If any sources are given they are searched as well.

        Only replacements with the name equal to this set's name are
        applied.
        {%name%} is replaced with the first match, {%name_2%} with the
        second match, and so on.

        - target is the text to replace in
        - If only_found is True then placeholders which didn't match
          are left as is rather than being replaced by the default
          value.

        Extracts found are saved in self.extracts
        '''

        logger.debug('Applying directives for {}'.format(self.name))

        self.search_sources(*sources)

        result = target.replace(
            decode_or_encode(self.get_placeholder(), target),
            decode_or_encode(self.get_placeholder(1), target))

        for i, e in enumerate(self.extracts, start=1):
            result = result.replace(
                decode_or_encode(self.get_placeholder(i), result),
                decode_or_encode(e.value, result))
            logger.trace('Replaced {} with {} -> {}'.format(
                self.get_placeholder(i), e, result))

        if only_found:
            logger.trace(
                'Leaving not found placeholders untouched')
            return result
        return re.sub(
            decode_or_encode(self.get_placeholder('*'), result),
            decode_or_encode(self.default, result),
            result)

    def _convert_value(self, key, value):
        logger.trace('Converting {} = {}'.format(key, value))
        if key not in self._implements:
            raise KeyError(
                '{} does not implement {}'.format(
                    self.__class__.__name__, key))

        try:
            value = self._conversions.get(key, lambda x: x)(value)
        except (TypeError, ValueError) as e:
            raise e.__class__(
                'Invalid value for {}: {!s}'.format(key, e))
        logger.trace('Converted value to {}'.format(value))

        allowed_types = self._type_constraints.get(key, type(value))
        if not isinstance(value, allowed_types):
            raise TypeError('{} must be one of types {}'.format(
                key, allowed_types))

        allowed_values = self._value_constraints.get(key)
        if allowed_values is not None:
            if is_seq_like(value):
                if set(value).intersection(
                        allowed_values) != set(value):
                    raise ValueError('{} can contain only {}'.format(
                        key, allowed_values))
            elif value not in allowed_values:
                raise ValueError('{} must be one of {}'.format(
                    key, allowed_values))

        return value

    def __repr__(self):
        return '{}({!r})'.format(self.__class__.__name__,
                                 self._directives)

    def __str__(self):
        return self.__repr__()

    def __contains__(self, key):
        return key in self._directives

    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        if attr.startswith('_'):
            super().__setattr__(attr, value)
            return

        self[attr] = value

    def __getitem__(self, key):
        return self._directives[key]

    def __setitem__(self, key, value):
        self._directives[key] = self._convert_value(key, value)

class ExtractDirectivesContainer(OrderedContainer):
    _holds = ExtractDirectives

    def __init__(self, *directive_sets, **kwargs):
        '''Parses a list of directive sets

        Each set is a dictionary of directive: value
        **kwargs are passed to the constructor of each directive
        '''

        super().__init__()
        for directives in directive_sets:
            self.new(**directives, **kwargs)

    def search_sources(self, *sources, **filter_kwargs):
        '''Searches sources and saves found extracts

        - If filter_kwargs are given, only the matching directives
          are applied.
        '''

        dsets = self.get(**filter_kwargs)
        for ds in dsets:
            ds.search_sources(*sources)

    def get(self, **filter_kwargs):
        '''Returns all directive sets filtered by the given arguments

        If an argument is given, e.g. stages=stage1, then only those
        directive sets which have the stage1 stages directive are
        returned. Filter arguments are joined as logical AND, but if
        any of the directives are lists, such as stages, then
        directives which have any of the given comma-separated stages
        are taken, i.e. list-like directive values are logical OR.
        '''

        result = []
        for ds in self:
            match = True
            for key, val in filter_kwargs.items():
                req_val = ds._convert_value(key, val)
                curr_val = ds[key]
                if is_seq_like(req_val):
                    # AND
                    #  match = set(req_val).intersection(
                    #      curr_val) == set(req_val)
                    # OR
                    match = bool(set(req_val).intersection(
                        curr_val))
                elif is_seq_like(curr_val):
                    match = req_val in curr_val
                else:
                    match = req_val == curr_val

                if not match:
                    break

            if match:
                result.append(ds)
        return result

    def apply(self, target, *sources, only_found=False, **filter_kwargs):
        '''Applies the replacements found so far to target text

        If any sources are given, they are searched as well.
        See ExtractDirectives.apply for the meaning of only_found.
        Directives are applied in order in which they have been added.

        - If filter_kwargs are given, only the matching directives
          are applied.
        '''

        dsets = self.get(**filter_kwargs)
        result = target
        for ds in dsets:
            result = ds.apply(result, *sources, only_found=only_found)
        return result
