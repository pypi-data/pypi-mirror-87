from collections import defaultdict
from typing import Any
import re

from .base import BaseDataClass

FILTER_EXPR_REGEX = r'([\w.]+)\s*([!><=~]{1,2})([\S\s]*)$'
OP_MAP = {
    '=': 'eq',
    '==': 'eq',
    '!=': 'neq',
    '<': 'lt',
    '<=': 'lte',
    '=<': 'lte',
    '>': 'gt',
    '>=': 'gte',
    '=>': 'gte',
    '~=': 'search'
}

ORDER_BY_EXPR_REGEX = r'([\w.]+)\s*(\+|-)'

class FilterFactory(object):
    def __init__(self, field_name):
        self.name = field_name

    def _filter(self, op, value):
        return Filter(
            name=self.name,
            op=op,
            val=value
        )
    
    def __eq__(self, value):
        return self._filter('eq', value)
        
    def __ne__(self, value):
        return self._filter('neq', value)

    def __lt__(self, value):
        return self._filter('lt', value)
        
    def __le__(self, value):
        return self._filter('lte', value)

    def __gt__(self, value):
        return self._filter('gt', value)

    def __ge__(self, value):
        return self._filter('gte', value)

    def match(self, regex):
        return self._filter('match', value)

    def search(self, regex):
        return self._filter('search', value)

class Filter(BaseDataClass):
    """A simple filter. Similar to SQLAlchemy filtrering system."""
    name: str
    op: str
    val: Any
    field_type: str = None

    @classmethod
    def from_expr(cls, expr):
        match = re.search(FILTER_EXPR_REGEX, expr)
        if not match:
            raise ValueError(f'Unable to parse expression {expr!r}')
        
        return cls(
            name=match.group(1).strip(),
            op=OP_MAP[match.group(2)],
            val=match.group(3).strip()
        )

    @classmethod
    def multi_from_declarative(cls, declarative_dict):
        """ With format:
        <name>:
            <op>: <val>
        <other name>:
            <op>: <val>
        ...
        """
        for name, op_val in declarative_dict.items():
            for op, val in op_val.items():
                yield cls(name=name, op=op, val=val)

    @staticmethod
    def multi_to_declarative(filters):
        result = defaultdict(dict)
        for f in filters:
            result[f.name][f.op] = f.val
        return result

    def inject_in_query(self, query):
        query.from_filters(self)

class OrderBy(BaseDataClass):
    name: str
    asc: bool
    
    @classmethod
    def from_expr(cls, expr):
        match = re.search(ORDER_BY_EXPR_REGEX, expr)
        if not match:
            raise ValueError(f'Unable to parse expression {expr!r}')
        
        asc = match.group(2).strip() == '+'

        return cls(
            name=match.group(1).strip(),
            asc=asc
        )


DEFAULT_OP_MAP_BY_FIELD_TYPE = {
    'string': ['eq', 'search'],
    'datetime': ['lt', 'gt']
}

class FilterSpec(BaseDataClass):
    name: str
    field_type: str
    input_type: str
    ops: list = list
    values: list = None
    label: str = None
    description: str = None

    def __post_init__(self):
        if not self.ops:
            self.ops = DEFAULT_OP_MAP_BY_FIELD_TYPE.get(self.field_type, ['eq'])