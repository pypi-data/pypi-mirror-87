import re

from typing import Dict, Any
from collections.abc import Mapping, Sequence, Mapping

from dataclasses import dataclass, fields, field, Field

from spintop.utils import GetRecursiveMixin, repr_obj

from .serialization import cls_of_serialized

def query_is(field_name, value):
    return QueryPart('set_value_equals', field_name, value)

def query_match(field_name, value):
    return QueryPart('set_value_match', field_name, value)

def query_is_one_of(field_name, values):
    return QueryPart('set_value_one_of', field_name, *values)

def query_list_contains(field_name, value):
    return QueryPart('set_list_contains', field_name, value)

def query_clear(field_name):
    return QueryPart('clear', field_name)

class QueryPart(object):
    def __init__(self, op, *args):
        self.op = op
        self.args = args

    def inject_in_query(self, query):
        fn = getattr(query, self.op)
        fn(*self.args)

class MultiQueryParts(object):
    def __init__(self, parts):
        self.parts = parts
    
    def inject_in_query(self, query):
        for part in self.parts:
            part.inject_in_query(query)

class FieldsOf(GetRecursiveMixin):
    def __init__(self, cls):
        self.type_ = cls
    
    def __iter__(self):
        for field in fields(self.type_):
            yield MetaField(self.type_, field)

    def __getattr__(self, key):
        field = self.get_field(key)
        return MetaField(self.type_, field)

    def get_field(self, key):
        if key == 'type_':
            raise RecursionError(key)
        cls = self.type_
        attr_value = getattr(cls, key, None)
        field = None
        
        try:
            fields_list = fields(cls)
        except TypeError:
            pass
        else:
            for possible_field in fields_list:
                if possible_field.name == key:
                    field = possible_field
                    break

        if isinstance(attr_value, property):
            try:
                field = PropertyField(attr_value, field=field)
            except TypeError as e:
                # add info
                raise TypeError(f'Property {key!r} of {cls} is invalid: {str(e)}')

        if field is None:
            raise AttributeError(f'No field named {key!r} in {cls}')
        else:
            return field

    def __eq__(self, other):
        try:
            return self.type_ == other.type_
        except AttributeError:
            return False

    def __repr__(self):
        return f'FieldsOf({self.type_.__name__})'

    def from_name(self, name):
        return self.get_recursive(name)

class CustomField():
    name = None
    type = None

    def accessor(self, name, obj):
        return getattr(obj, name)

    def setter(self, obj, value):
        return 

    def __repr__(self):
        return repr_obj(self, ['name', 'type'])

class PropertyField(CustomField):
    def __init__(self, property_attr, field=None):
        if field:
            self.name = field.name
            self.type = field.type
        else:
            self.name = property_attr.fget.__name__
            annotations = property_attr.fget.__annotations__

            if 'return' not in annotations:
                raise TypeError('Property field must declare the return type to be used as a meta field.')

            self.type = annotations['return']

class DictField(CustomField):
    def __init__(self, key):
        self.name = key
        self.type = Any

    def accessor(self, name, obj):
        return obj[name]

    def setter(self, obj, name, value):
        obj[name] = value

class MetaField():
    def __init__(self, cls, field, parents=()):
        self.__type = cls
        self.__parents = parents
        self.__field = field
    
    @property
    def __doc__(self):
        return self.__type.field_doc(self.field_name_)

    @property
    def field_name_(self):
        return self.__field.name

    @property
    def name_(self):
        return '.'.join(self.name_tuple_)

    @property
    def type_(self):
        return self.__field.type

    @property
    def field_(self):
        return self.__field

    @property
    def container_type_(self):
        return self.__type

    @property
    def root_container_type_(self):
        if self.__parents:
            return self.__parents[0].__type
        else:
            return self.__type

    @property
    def meta_fields_(self):
        return self.__parents + (self,)

    @property
    def name_tuple_(self):
        return tuple(meta_field.__field.name for meta_field in self.meta_fields_) 
    
    def __call__(self, obj):
        return self.get_value(obj)

    def get_value(self, obj):
        return self._get_value(
            obj, 
            context=dict(
                is_serialized=isinstance(obj, Mapping)
            )
        )

    def _get_value(self, obj, context, meta_fields=None):
        if meta_fields is None:
            meta_fields = self.meta_fields_

        for meta_field in meta_fields:
            accessor = meta_field.obj_accessor_factory(**context)
            obj = accessor(obj)
        return obj

    def set_value(self, obj, value):
        return self._set_value(
            obj, 
            value, 
            context=dict(
                is_serialized=isinstance(obj, Mapping)
            )
        )

    def _set_value(self, obj, value, context):
        meta_fields_except_last = self.meta_fields_[:-1]
        last_meta_field = self.meta_fields_[-1]
        if meta_fields_except_last:
            obj = self._get_value(obj, context, meta_fields=meta_fields_except_last)

        setter = last_meta_field.obj_setter_factory(**context)
        setter(obj, value)

    def obj_accessor_factory(self, is_serialized):
        if is_serialized:
            return self.serialized_accessor
        else:
            return self.obj_accessor

    def obj_accessor(self, obj): 
        self._check_type(obj.__class__)
        return getattr(obj, self.field_name_)

    def serialized_accessor(self, obj): 
        # No type check when serialized.
        # self._check_type(cls_of_serialized(obj))
        return obj[self.field_name_]   

    def _check_type(self, obj_cls):
        if obj_cls is None or not self.is_type_of_cls(obj_cls):
            raise AttributeError(f'Obj cls {obj_cls} does not match expected {self.container_type_}')

    def obj_setter_factory(self, is_serialized):
        if is_serialized:
            return self.serialized_setter
        else:
            return self.obj_setter
        
    def obj_setter(self, obj, value): 
        self._check_type(obj.__class__)
        setattr(obj, self.field_name_, value)

    def serialized_setter(self, obj, value):
        # No type check when serialized.
        obj[self.field_name_] = value

    def is_type_of_cls(self, cls):
        return cls is self.__type or issubclass(cls, self.__type)

    def is_container_of_cls(self, cls):
        return cls is self.root_container_type_ or issubclass(cls, self.root_container_type_)

    def __getattr__(self, key):
        cls = self.__field.type
        field = FieldsOf(cls).get_field(key)
        return self.__class__(cls, field, parents=self.meta_fields_)

    def __getitem__(self, key):
        cls = self.__field.type
        try:
            is_dict = issubclass(cls, Dict)
        except TypeError:
            is_dict = 'dict' in cls._name.lower()

        if is_dict:
            return DictMetaField(cls, DictField(key), parents=self.meta_fields_)
        else:
            try:
                return getattr(self, key)
            except AttributeError:
                raise KeyError(key)

    def __hash__(self):
        return hash(self.__field)

    def __repr__(self):
        return f'MetaField({self.root_container_type_.__name__}.{self.name_})'

    ## Query Building
    
    def __eq__(self, other):
        """When compared to another MetaField, check for equality and returns a Boolean.
        
        When compared to other types, returns a QueryPart to be used in a query."""
        if isinstance(other, MetaField):
            # Normal comparaison
            return self.__field == other.__field
        else:
            # Query comparaison
            query_value = other
            return self.is_(query_value)

    def __ge__(self, query_value):
        """For mappings: field >= {'x': 'y'}. 
        
        Contains at least the mapping exactly."""
        parts = self._build_mapping_parts(query_value)
        return MultiQueryParts(parts)

    def _build_mapping_parts(self, value):
        parts = []
        if isinstance(value, Mapping):
            for key, value in value.items():
                field = self[key]
                parts += field._build_mapping_parts(value)
        else:
            parts.append(self.__eq__(value))
        return parts

    def __le__(self, query_value):
        return self.one_of_(query_value)

    def is_(self, value):
        # value = getattr(value, , value)
        if hasattr(value, 'pattern'):
            # for regexes.
            return query_match(self.name_, value.pattern) # deconstruct re.compile to allow serialization
        else:
            return query_is(self.name_, value)

    def one_of_(self, value):
        return query_is_one_of(self.name_, value)

    def contains_(self, value):
        return query_list_contains(self.name_, value)

    def any_(self):
        return query_clear(self.name_)
    

class DictMetaField(MetaField):
    
    def obj_accessor(self, obj): 
        return obj[self.field_name_]

    def serialized_accessor(self, obj): 
        obj_cls = obj.__class__
        if not isinstance(obj, Mapping):
            raise AttributeError(f'Obj cls {obj_cls} should be a Mapping.')
        return obj[self.field_name_]   
        
    def obj_setter(self, obj, value): 
        obj[self.field_name_] = value

def _get_value_fields(obj, accessor, meta_fields):
    for meta_field in meta_fields:
        accessor_fn = getattr(meta_field, accessor)
        obj = accessor_fn(obj)
    return obj
