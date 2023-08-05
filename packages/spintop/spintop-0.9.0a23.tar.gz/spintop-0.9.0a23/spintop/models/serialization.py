import dateutil.parser
import pytz

from json import dumps, loads

from copy import copy
from typing import Union, NamedTuple
from collections import OrderedDict, defaultdict
from collections.abc import Sequence, Mapping, MappingView
from functools import lru_cache
from datetime import datetime

from marshmallow import Schema, fields, pre_load, post_dump, EXCLUDE, ValidationError
from marshmallow_jsonschema import JSONSchema

from spintop.utils.marshmallow_dataclass import class_schema
from spintop.utils.marshmallow_oneofschema import OneOfSchema

from spintop.utils import local_tz, isnan, dict_ops

_TYPE_TO_CLS_MAP = {}
_SCHEMA_TYPES = {}

TYPE_KEY = '_type'

_TYPE_CLS_CHILDREN = defaultdict(set)

_REGISTERED_TYPES = []

def register_type(cls, _type=None, schema_cls=None):
    if _type is None:
        _type = cls.__name__
    cls._type = _type
    
    if _type in _TYPE_TO_CLS_MAP and _TYPE_TO_CLS_MAP[_type] != cls:
        raise ValueError("Type %s is already registered to class %s" % (_type, _TYPE_TO_CLS_MAP[_type]))

    _TYPE_TO_CLS_MAP[_type] = cls

    _REGISTERED_TYPES.append((cls, schema_cls))

    for schema_key in _SCHEMA_TYPES:
        Schema = DataClassSchema(cls, schema_type=get_base_schema_cls(schema_key), schema_cls=schema_cls)

        # Building the schema now improves serialization performance by up to 800%
        _SCHEMA_TYPES[schema_key].type_schemas[_type] = Schema()

    for other_cls in _TYPE_CLS_CHILDREN:
        if other_cls in cls.__mro__:
            _TYPE_CLS_CHILDREN[other_cls].add(cls)
    _TYPE_CLS_CHILDREN[cls] = _TYPE_CLS_CHILDREN[cls]

def cls_subclasses(cls):
    """Returns a set containing the subclasses of cls 
    (if cls was at some point passed to register_type as argument)"""
    return _TYPE_CLS_CHILDREN[cls]

def cls_of_obj(obj):
    if isinstance(obj, Mapping):
        return cls_of_serialized(obj)
    else:
        return obj.__class__
    # try:
    #     _type = type_of(obj)
    #     cls = cls_of_type(_type)
    #     if cls is None:
    #         raise AttributeError(f'{cls} is not mapped to a type')
    #     return cls
    # except AttributeError:
    #     return cls_of_serialized(obj)

def cls_of_serialized(obj_serialized):
    return cls_of_type(serialized_type_of(obj_serialized))

def cls_of_type(_type):
    return _TYPE_TO_CLS_MAP.get(_type, None)

def type_of(cls):
    return cls._type

def serialized_type_of(obj_serialized):
    return obj_serialized[TYPE_KEY]

def type_dict_of(cls):
    return {TYPE_KEY: type_of(cls)}

def is_type_of(cls, base_cls):
    return type_of(cls) == type_of(base_cls)

def is_serialized_type_of(obj_serialized, base_cls):
    return serialized_type_of(obj_serialized) == type_of(base_cls)

def get_serializer(schema_key=None):
    return Serializer(get_base_schema_cls(schema_key))

@lru_cache(maxsize=None)
def DataClassSchema(cls, schema_type=None, schema_cls=None):
    if schema_cls:
        schema_cls = compose_schema_cls(schema_type, schema_cls)
    else:
        schema_cls = schema_type
    schema = class_schema(cls, base_schema=schema_cls)
    return schema

def get_base_schema_cls(schema_key):
    try:
        return _SCHEMA_TYPES[schema_key]
    except KeyError:
        raise ValueError(f'Schema key {schema_key!r} not in supported list: {_SCHEMA_TYPES.keys()!r}')

def compose_schema_cls(base, child):
    return type(f'Composed{child.__name__}', (base, child), {})

class Serializer(object):
    def __init__(self, base_schema_cls):
        self.base_schema_cls = base_schema_cls

    def schema(self, *args, cls=None, strict_casting=None, **kwargs):
        schema = self.base_schema_cls(*args, **kwargs)
        
        if strict_casting is not None:
            schema.context['strict_casting'] = strict_casting
        if cls:
            schema.context.update(type_dict_of(cls))
        
        return schema

    def serialize_barrier(self, raw_records, validate=True, cls=None):
        raw_records = list(raw_records)
        schema = self.schema(many=True, cls=cls)

        if raw_records and not isinstance(raw_records[0], Mapping):
            records = schema.dump(raw_records)
        else:
            records = raw_records

        if validate:
            validation = schema.validate(records)
            if validation:
                raise ValidationError(validation)
        
        return records

    def serialize(self, obj, cls=None, strict_casting=None):
        master_schema = self.schema(cls=cls, strict_casting=strict_casting)

        try:
            type_of(obj) # Tests if it has a _type attribute.
        except (AttributeError, TypeError):
            return self.serialize_primitive(obj)
        else:
            return master_schema.dump(obj)

    def deserialize(self, obj, cls=None, strict_casting=None, **kwargs):
        master_schema = self.schema(cls=cls, strict_casting=strict_casting)
        return master_schema.load(obj, **kwargs)

    def serialize_primitive(self, obj):
        if isinstance(obj, Sequence) and not isinstance(obj, str):
            return [self.serialize(subobj) for subobj in obj]
        elif isinstance(obj, Mapping):
            return {key: self.serialize(value) for key, value in obj.items()}
        else:
            try:
                Field = self.base_schema_cls.TYPE_MAPPING[type(obj)]
            except KeyError:
                # No mapped field. Return as-is !
                return obj
            field = Field()
            return field._serialize(obj, None, None)

    def deserialize_primitive(self, obj, cls=None):
        if isinstance(obj, Sequence):
            return [self.deserialize(subobj, cls=cls) for subobj in obj]
        elif isinstance(obj, Mapping):
            return {key: self.deserialize(value, cls=cls) for key, value in obj.items()}
        else:
            raise ValueError('Unable to deserialize primitives other than list or dict.')


class NoopDatetime(fields.AwareDateTime):
    def _serialize(self, value, attr, obj, **kwargs):
        return value

    def _deserialize(self, value, attr, data, **kwargs):
        return value

class OrderedDictField(fields.Mapping):
    def _serialize(self, value, attr, obj, **kwargs):
        value_as_dict = dict(value)
        serialized_as_dict = super()._serialize(value_as_dict, attr, obj, **kwargs)
        return [(key, serialized_as_dict[key]) for key in value]

    def _deserialize(self, list_value, attr, data, **kwargs):
        value_as_dict = {key: value for key, value in list_value}
        deserialized_as_dict = super()._deserialize(value_as_dict, attr, data, **kwargs)
        result = OrderedDict()
        for key, _ in list_value:
            result[key] = deserialized_as_dict[key]
        return result

class FloatFieldNoNaN(fields.Float):
    def _serialize(self, value, attr, data, **kwargs):
        if value is None or isnan(value):
            value = None
        num = super()._serialize(value, attr, data, **kwargs)
        return num

class AwareDateTimeDeserializeNoop(fields.AwareDateTime):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, default_timezone=pytz.utc, **kwargs)

    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, datetime):
            return value.replace(tzinfo=self.default_timezone)
        else:
            return super()._deserialize(value, attr, data, **kwargs)

class DictJsonField(fields.Dict):
    def _serialize(self, value, attr, obj, **kwargs):
        if value:
            return dumps(super()._serialize(value, attr, obj, **kwargs))
        else:
            return '{}' # Empty json

    def _deserialize(self, value, attr, data, **kwargs):
        if value is None:
            return {}
        else:
            return super()._deserialize(loads(value), attr, data, **kwargs)

def base_type_mapping(additions={}):
    default_type_mapping = copy(Schema.TYPE_MAPPING)
    default_type_mapping.update({
        float: FloatFieldNoNaN,
        OrderedDict: OrderedDictField,
        datetime: AwareDateTimeDeserializeNoop,
        list: fields.List,
        set: fields.List,
        tuple: fields.Tuple,
        dict: fields.Dict
    })

    try:
        from pandas import Timestamp
    except ImportError:
        pass
    else:
        default_type_mapping.update({
            Timestamp: AwareDateTimeDeserializeNoop
        })

    default_type_mapping.update(additions)
    return default_type_mapping

class AbstractSchema(OneOfSchema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    type_schemas = {}
    TYPE_MAPPING = base_type_mapping()
    type_field = TYPE_KEY
    _attached = False

    _type = fields.String(dump_only=True)

    def __new__(cls, *args, **kwargs):
        if not cls._attached:
            cls.attach_registered_dataclasses()
        obj = super().__new__(cls)
        obj.__init__(*args, **kwargs)
        return obj

    def get_obj_type(self, obj):
        # If a mapping, returns the class from the _type attribute
        # If an object, returns the class itself.
        cls = cls_of_obj(obj) 
        if cls is None:
            return None
        else:
            # Return the string registered to that cls.
            return type_of(cls)

    @classmethod
    def build_schema_type(cls, name_or_base_cls, additional_type_mapping=None, _type_mapping=None):
        if _type_mapping is None:
            if additional_type_mapping is None:
                additional_type_mapping = {}
            _type_mapping = base_type_mapping(additional_type_mapping)

        cls_dict = {
            'type_schemas': {},
            'TYPE_MAPPING': _type_mapping
        }

        if isinstance(name_or_base_cls, type):
            name = name_or_base_cls.__name__
            base_cls = (cls, name_or_base_cls)
        else:
            name = name_or_base_cls
            base_cls = (cls,)

        schema_type = type(name, base_cls, cls_dict)
        schema_type.attach_registered_dataclasses()
        return schema_type
    
    @classmethod
    def attach_registered_dataclasses(cls):
        cls.type_schemas = {}
        cls._attached = True

        for data_cls, schema_cls in _REGISTERED_TYPES:
            Schema = DataClassSchema(data_cls, schema_type=cls, schema_cls=schema_cls)

            # Building the schema now improves serialization performance by up to 800%
            cls.type_schemas[data_cls._type] = Schema()
        


def register_schema_type(key, schema_type, _default=False):
    if key in _SCHEMA_TYPES:
        raise ValueError(f'Key {key!r} is already registered.')

    _SCHEMA_TYPES[key] = schema_type

    if _default:
        _SCHEMA_TYPES[None] = schema_type

    return schema_type
    

JsonCompatSchema = AbstractSchema.build_schema_type(
    'JsonCompatSchema'
)

BsonCompatSchema = AbstractSchema.build_schema_type(
    'BsonCompatSchema',
    {
        datetime: NoopDatetime # keeps datetime as is
    }
)

DeepTabularCompatSchema = AbstractSchema.build_schema_type(
    'DeepTabularCompatSchema',
    {
        dict: DictJsonField # Serialize dicts to JSON. Required to have a constant schema.
    }
)

register_schema_type('tabular', DeepTabularCompatSchema)
register_schema_type('json', JsonCompatSchema)
register_schema_type('bson', BsonCompatSchema, _default=True)



def get_bson_serializer():
    return get_serializer('bson')

def get_json_serializer():
    return get_serializer('json')

class SerializedWrapper(dict_ops.DictWrapper):
    
    @property
    def type_(self):
        return self[TYPE_KEY]

    @type_.setter
    def type_(self, value):
        self[TYPE_KEY] = value

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

## JSON Schema generation

@lru_cache(maxsize=None)
def dump_json_schema(cls):
    schema = cls.get_schema()()
    json_schema_generator = JSONSchema(props_ordered=True)
    return expand_schema_refs(json_schema_generator.dump(schema))

def expand_schema_refs(json_schema, _original=None):
    if _original is None:
        _original = json_schema
    
    if '$ref' in json_schema:
        definition_path = json_schema['$ref'].split('/')[1:] # Remove first '#'
        reference_content = _original
        for p in definition_path:
            reference_content = reference_content[p]

        json_schema.update(reference_content)
        json_schema.pop('$ref')
    
    json_schema.pop('$schema', None)

    for key, value in json_schema.items():
        if isinstance(value, Mapping):
            json_schema[key] = expand_schema_refs(value, _original=_original)

    return json_schema

