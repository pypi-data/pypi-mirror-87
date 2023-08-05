import json

from typing import Callable, Type
from copy import copy
from contextlib import contextmanager
from dataclasses import dataclass

from spintop.analytics.base import REQUEST_ID, AbstractSingerTarget

from spintop.logs import _logger

ORG_ID_KEY = '_group'

logger = _logger('analytics')

@dataclass()
class ReservedStream():
    callback: Callable = None
    stream_type: Type = None
    stream_name: str = None

class ContextualAnalyticsTarget(AbstractSingerTarget):
    def __init__(self, analytics, reserved_streams=None, unlocked_streams=None, request_id=None, org_id=None):
        self.analytics = analytics
        if reserved_streams is None:
            reserved_streams = {}

        super().__init__()
        self.request_id = request_id
        self.org_id = org_id

        self.analytics = analytics
        self.reserved_streams = reserved_streams
        # self.unlocked_streams = unlocked_streams

    @property
    def reserved_stream_names(self):
        return set(self.reserved_streams.keys())

    def reserve_stream_name(self, name, callback=None, stream_type=None, stream_name=None):
        if stream_name is None:
            stream_name = name
        self.reserved_streams[name] = ReservedStream(callback=callback, stream_type=stream_type, stream_name=stream_name)

    def get_reserved_stream(self, name):
        return self.reserved_streams.get(name, ReservedStream())

    def unlock_target(self, unlock_stream_names=None, request_id=None, org_id=None):

        return self.__class__(
            self.analytics,
            reserved_streams=self.reserved_streams,
            unlocked_streams=unlock_stream_names,
            request_id=request_id,
            org_id=org_id
        )

    def update_named_stream(self, name, raw_data, stream_type=None):
        reserved_stream = self.get_reserved_stream(name)
        reserved_stream_type = reserved_stream.stream_type
        if stream_type and reserved_stream_type and reserved_stream_type != stream_type:
            raise ValueError(f'Mismatch between request stream type {stream_type!r} and reserved stream type {reserved_stream_type!r}')
        response = self.unlock_target({name})._update_named_endpoint_unlocked(reserved_stream.stream_name, raw_data, reserved_stream_type)
        if reserved_stream.callback:
            reserved_stream.callback(self.analytics.functions)
        return response

    def _update_named_endpoint_unlocked(self, name, raw_data, stream_type):
        return super().update_named_stream(name, raw_data, stream_type)

    @property
    def functions(self):
        return self.analytics.functions

    def send_messages_dict(self, messages_dict, request_id=None, stream_name=None):
        valid_messages, stream_names = self._validate_messages(messages_dict)
        response = self.analytics.send_messages_dict(
            valid_messages, 
            request_id=request_id if request_id else self.request_id, 
            stream_name=stream_name
        )
        return response

    def _validate_messages(self, messages_dict):
        validated_messages = []
        stream_names = set()
        for content in messages_dict:
            stream_name = content.get('stream')

            # self.assert_not_reserved(stream_name)
            
            stream_names.add(stream_name)
            content = self._message_transform(content)

            validated_messages.append(content)
        
        return validated_messages, stream_names
    
    def assert_not_reserved(self, stream_name):
        for reserved_stream in self.reserved_stream_names:
            if stream_name.startswith(reserved_stream):
                raise ValueError(f'Stream with name {stream_name!r} is reserved for internal use. No stream may start with {reserved_stream!r}.')

    def _message_transform(self, message_content):
        msg_type = message_content['type']
        if msg_type == 'SCHEMA':
            message_content['schema']['properties'][ORG_ID_KEY] = {'type': 'string'}
            message_content['key_properties'] = message_content.get('key_properties', []) + [ORG_ID_KEY]
        elif msg_type == 'RECORD':
            message_content['record'][ORG_ID_KEY] = self.org_id
            message_content['record'][REQUEST_ID] = self.request_id
        else:
            raise ValueError(f'Unsupported message type: {msg_type}')
        return message_content
