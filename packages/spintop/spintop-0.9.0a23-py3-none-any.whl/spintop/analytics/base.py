import re
import datetime as dt
from time import time
from functools import lru_cache
from collections.abc import Mapping
import json

from copy import deepcopy
from contextlib import contextmanager

from spintop.models.serialization import get_serializer, get_json_serializer
from spintop.utils import utcnow_aware, dict_ops

from .models import AnalyticsResponse
from . import singer
from ..logs import _logger

logger = _logger('singer')

DATETIME_TYPE = {'type': 'string', 'format': 'date-time'}

REQUEST_ID = '_spintop_request_id'

SCHEMA_ADDITIONS = {
    singer.SEQUENCE : {"type": "integer"},
    singer.BATCHED_AT: DATETIME_TYPE,
    REQUEST_ID: {"type": "string"}
}

@lru_cache()
def utcdatetime(_currenttime):
    """Computed only if current time changes."""
    return utcnow_aware()

class SingerMessagesFactory(object):
    def __init__(self, stream_name, add_null_to_fields=True):
        self.stream_name = stream_name
        self.transform_schema_kwargs = dict(
            add_null_to_fields=add_null_to_fields
        )
        self.logger = logger.getChild(stream_name)

    def get_default_schema(self):
        return None

    def schema(self, schema , key_properties):
        schema = deepcopy(schema)
        schema['properties'].update(SCHEMA_ADDITIONS)
        _schema_transform(schema, **self.transform_schema_kwargs)
        schema = change_keys_deep(schema, sanitize_key)
        return {
            'type': 'SCHEMA',
            'stream': self.stream_name,
            'key_properties': key_properties,
            'schema': schema
        }

    def record(self, data):
        current_time = sdc_sequence_now()
        data.update({
            singer.SEQUENCE: current_time,
            singer.BATCHED_AT: utcdatetime(current_time).isoformat() # serialize right away
        })

        data = change_keys_deep(data, sanitize_key, remove_none)
        return {
            'type': 'RECORD',
            'stream': self.stream_name,
            'record': data
        }

def sdc_sequence_now():
    return int(time()*1000*1000)

class ModelSingerMessagesFactory(SingerMessagesFactory):
    def __init__(self, stream_name, record_cls, serializer, **kwargs):
        self.record_cls = record_cls
        self.serializer = serializer
        super().__init__(stream_name, **kwargs)

    def get_default_schema(self):
        jsonschema = self.record_cls.dump_json_schema()
        return super().schema(jsonschema, key_properties=[])

    def schema(self, *args, **kwargs):
        raise TypeError('Model based message factory cannot receive a schema.')

    def record(self, data):
        """Data should be of type self.record_cls"""
        serialized = self.serializer.serialize(data, self.record_cls)
        return super().record(serialized)

class _NamedEndpointAccessor(object):
    def __init__(self, name):
        self.name = name
    
    def __get__(self, obj, cls):
        return NamedEndpoint(
            name=self.name,
            analytics=obj
        )

class NamedEndpoint(object):
    def __init__(self, name, analytics):
        self.name = name
        self.analytics = analytics
    
    def singer_factory(self):
        return self.analytics.singer_factory(self.name)

    def update(self, data):
        return self.analytics.update_named_stream(self.name, data)

class AbstractAnalyticsTarget(object):
    add_null_to_fields = False

    steps = _NamedEndpointAccessor('steps')
    features = _NamedEndpointAccessor('features')
    
    def __init__(self):
        self.serializer = get_serializer('tabular')
    
    def get_endpoint(self, name):
        return getattr(self, name)

    def update_named_stream(self, name, records, stream_type=None):
        with self.stream(name, stream_type) as batch:
            for record in records:
                batch.record(record)

    @property
    def functions(self):
        return None # To be overwritten

    @contextmanager
    def stream(self, stream_name, record_cls=None):
        batch = self.begin_batch(stream_name, record_cls=record_cls)
        yield batch
        batch.result = self.flush_batch(batch)

    def begin_batch(self, stream_name, record_cls=None):
        factory = self.singer_factory(stream_name, record_cls)
        return self.collect_factory(factory)

    def collect_factory(self, factory):
        return CollectMessagesFromFactory(factory)

    def singer_factory(self, stream_name, record_cls=None):
        if record_cls:
            return ModelSingerMessagesFactory(
                stream_name,
                record_cls,
                serializer=self.serializer,
                add_null_to_fields=self.add_null_to_fields
            )
        else:
            return SingerMessagesFactory(
                stream_name,
                add_null_to_fields=self.add_null_to_fields
            )

    def flush_batch(self, batch):
        raise NotImplementedError()
    
    def complete_response(self, response, request_id, stream_name):
        if request_id and not response.request_id:
            response.request_id = request_id

        if stream_name and not response.stream_name:
            response.stream_name = stream_name
        
        return response

class AbstractSingerTarget(AbstractAnalyticsTarget):
    
    def flush_batch(self, batch):
        singer_messages = batch.records
        if batch.schema:
            singer_messages.insert(0, batch.schema)

        batch.result = self.send_messages_dict(singer_messages, stream_name=batch.stream_name)

    def send_messages_dict(self, messages_dict, request_id=None, stream_name=None):
        return self.send_messages(self.json_dumps_messages(messages_dict), stream_name=stream_name)

    def send_messages(self, messages_str, request_id=None, stream_name=None):
        raise NotImplementedError()

    def json_dumps_messages(self, messages):
        serialized_messages = [self.serializer.serialize(msg) for msg in messages]
        return [json.dumps(ser_msg) for ser_msg in serialized_messages]

class CollectMessagesFromFactory(object):
    def __init__(self, factory):
        self.schema = factory.get_default_schema()
        self.records = []
        self.result = None
        self.factory = factory

    @property
    def stream_name(self):
        return self.factory.stream_name

    def schema(self, *args, **kwargs):
        if self.schema:
            raise ValueError('Message collector only supports one schema per batch.')
        
        self.schema = self.factory.schema(*args, **kwargs)
        return self.schema

    def record(self, *args, **kwargs):
        record = self.factory.record(*args, **kwargs)
        self.records.append(record)
        return record

### Replace datetime by string type.
_FIELD_TRANSFORM = {
    'datetime': lambda field: DATETIME_TYPE
}

def _schema_transform(schema, add_null_to_fields=True):
    try:
        fields = schema.get('properties', {})
    except AttributeError:
        return 
    
    for key, field in fields.items():
        # Try to get type in map, else keep same.
        # Also add null allowed everywhere.
        field.pop('default', None)
        most_important_field_type = get_field_type(field['type'])

        transformer = _FIELD_TRANSFORM.get(most_important_field_type, None)
        if transformer:
            update = transformer(field)
            field.update(update)

        if add_null_to_fields:
            field['type'] = [most_important_field_type, 'null']

        # in case it contains other properties (object)
        _schema_transform(field, add_null_to_fields=add_null_to_fields)

def get_field_type(field_type):
    if isinstance(field_type, str):
        return field_type
    elif field_type:
        for possible_type in field_type:
            if possible_type.lower() != 'null':
                return possible_type
    
    # Else
    return None


class RemoveValue(Exception):
    pass

def sanitize_key(key):
    return key.replace('.', '_')

def remove_none(value):
    if value is None:
        raise RemoveValue()
    else:
        return value

def noop(value):
    return value

def change_keys_deep(dict_obj, key_op, value_op=noop):
    new_flat = {}
    flat = dict_ops.flatten_dict(dict_obj)
    for key_tuple, value in flat.items():
        new_key_tuple = tuple(key_op(key) for key in key_tuple)
        try:
            new_flat[new_key_tuple] = value_op(value)
        except RemoveValue:
            pass

    return dict_ops.deepen_dict(new_flat)

DATETIME_REGEX = re.compile(r'(?:\D|^)(\d{4})-?([0-1]\d)-?([0-3]\d)(?:\D|$)')

def get_uuid_datetime(uuid):
    match = DATETIME_REGEX.search(uuid)
    if not match:
        raise ValueError('uuid does not contain a date in ISO format yyyymmdd or yyyy-mm-dd')
    
    try:
        year = int(match.group(1))
        month = int(match.group(2))
        day = int(match.group(3))
    except ValueError as e:
        raise ValueError(f'Unable to cast string to int: {str(e)}')

    try:
        return dt.datetime(year=year, month=month, day=day)
    except ValueError as e:
        raise ValueError(f'{year}-{month}-{day} is an invalid date: {str(e)}')