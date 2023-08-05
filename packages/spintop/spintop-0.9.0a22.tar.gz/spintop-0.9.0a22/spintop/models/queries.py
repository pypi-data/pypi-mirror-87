import re
from typing import List

from functools import wraps
from collections import OrderedDict, defaultdict
from collections.abc import Sequence

from .serialization import get_json_serializer, type_of, TYPE_KEY

from .base import BaseDataClass

from .filtering import Filter, OrderBy

from spintop.utils.dict_ops import (
    update,
    deepen_dict,
    flatten_dict,
    tuplify_key
)

def record_call():
    def _record_call(fn):
        @wraps(fn)
        def _recorded(self, field_name, *args):
            self._record_call(fn.__name__, field_name, args)
            return fn(self, field_name, *args)
        return _recorded
    return _record_call

class QueryData(BaseDataClass):
    _calls : OrderedDict = OrderedDict

class QueryResult(BaseDataClass):
    rows: List[dict] = list
    query_id: str
    filters: List[Filter] = list
    orderby: List[OrderBy] = list
    query_type: str = None
    total_rows_count: int = None
    rows_count: int = None
    page_token: str = None
    next_page_token: str = None

class BaseQuery():

    def __init__(self, parts=[], *other_parts):
        # The field key must equal exactly value, or re.search if a compiled regex
        self._value_equals = dict()

        # The field of type list named key must contain value
        self._list_contains = dict()

        # The field named key must equal one of the sub value in the list value
        self._value_equals_one_of = dict()

        self._calls = OrderedDict()


        if not isinstance(parts, Sequence):
            parts = [parts]

        parts = list(self.default_parts()) + parts

        for query_part in tuple(parts) + other_parts:
            self.add(query_part)

    @property
    def value_equals(self):
        return self._value_equals

    @property
    def list_contains(self):
        return self._list_contains

    @property
    def value_equals_one_of(self):
        return self._value_equals_one_of

    def default_parts(self):
        """To override"""
        return []

    def add(self, query_part):
        query_part.inject_in_query(self)

    def _record_call(self, fn_name, field_name, arg):
        fn_name_and_key = self.KEY_SEPARATOR.join((fn_name, field_name))
        self._calls[fn_name_and_key] = arg

    def add_call(self, fn_name_and_key, args):
        fn_name, key = fn_name_and_key.split(self.KEY_SEPARATOR)
        getattr(self, fn_name)(key, *args)

    # Raw calls

    @record_call()
    def set_value_equals(self, field_name, value):
        self._value_equals[field_name] = value

    @record_call()
    def set_value_match(self, field_name, value):
        self._value_equals[field_name] = re.compile(value)

    @record_call()
    def set_value_one_of(self, field_name, *values):
        self._value_equals_one_of[field_name] = values

    @record_call()
    def set_list_contains(self, list_field_name, value):
        self._list_contains[list_field_name] = value

    @record_call()
    def clear(self, field_name, value=None):
        for _dict in (self.value_equals, self.value_equals_one_of, self.list_contains):
            _dict.pop(field_name, None)

    def __eq__(self, other_q):
        same_len = len(self._calls) == len(other_q._calls)
        if not same_len:
            return False

        for key, value in self._calls.items():
            if key not in other_q._calls or other_q._calls[key] != value:
                return False
        
        return True

    def __repr__(self):
        return '{}(eq={}, oneof={}, contains={})'.format(
            self.__class__.__name__,
            repr(self._value_equals),
            repr(self._value_equals_one_of),
            repr(self._list_contains)
        )

    KEY_SEPARATOR = '::'
    def as_dict(self):
        serializer = get_json_serializer()

        list_of_calls = serializer.serialize(QueryData(_calls=self._calls))['_calls']
        # TODO keep order of calls

        return {key: value for key, value in list_of_calls}

    @classmethod
    def from_dict(cls, _flat_separated_calls):
        query = cls()
        for fn_name, args in _flat_separated_calls.items():
            query.add_call(fn_name, args)
        return query

    def copy(self):
        return self.__class__.from_dict(self.as_dict())

def multi_query_serialize(**queries):
    """ Serialized as key_subkey = subvalue for key key, query in queries.
    """

    result = {}

    for key, query in queries.items():
        if BaseQuery.KEY_SEPARATOR in key:
            raise ValueError('Query key {!r} cannot contain {!r}.'.format(key, Query.KEY_SEPARATOR))
        if query:
            for subkey, subvalue in query.as_dict().items():
                result[BaseQuery.KEY_SEPARATOR.join((key, subkey))] = subvalue
    
    return result

def multi_query_deserialize(_dict):
    queries = {}

    for key, value in _dict.items():
        query_name, fn_name = split_key(key)
        update(queries, {
            query_name: {fn_name: value}
        })
    
    return {query_name: BaseQuery.from_dict(query_dict) for query_name, query_dict in queries.items()}

def split_key(key):
    split_key = key.split(BaseQuery.KEY_SEPARATOR)
    return split_key[0], BaseQuery.KEY_SEPARATOR.join(split_key[1:])