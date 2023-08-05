
from enum import Enum
from functools import wraps
from collections import defaultdict
from collections.abc import Mapping

from collections import namedtuple

from .models import PersistenceRecordsUpdateMessage

Topic = namedtuple('Topic', ('name', 'message_cls'))

class Topics(Enum):
    RECORDS_UPDATE_TOPIC = Topic(name='records.update', message_cls=PersistenceRecordsUpdateMessage)

def messages_endpoint(topic):
    return property(
        fget = lambda publisher: _MessagesEndpoint(publisher, topic)
    )

class SpintopMessagePublisher(object):
    records_update = messages_endpoint(Topics.RECORDS_UPDATE_TOPIC)

    def subscribe(self, topic, callback):
        raise NotImplementedError()

    def publish(self, topic, message):
        raise NotImplementedError()

    def prepare_message(self, message):
        pass

    def supports_publish(self):
        return True

    def supports_subscribe(self):
        return True

class _MessagesEndpoint(object):
    def __init__(self, publisher, topic_obj):
        topic_obj = topic_obj.value
        
        topic = topic_obj.name
        message_model_cls = topic_obj.message_cls

        self.publisher = publisher
        self.topic = topic
        self.schema = message_model_cls.get_schema('json')()

    def subscribe(self, callback):
        if self.publisher.supports_subscribe():
            @wraps(callback)
            def _wrapper(raw_message):
                message = self.load_message(raw_message)
                callback(message)

            self.publisher.subscribe(self.topic, _wrapper)

    def dump_message(self, message):
        if isinstance(message, Mapping):
            return message
        else:
            return self.schema.dump(message)

    def load_message(self, raw_message):
        return self.schema.load(raw_message)

    def publish(self, message):
        if self.publisher.supports_publish():
            self.publisher.prepare_message(message)
            content = self.dump_message(message)
            self.publisher.publish(self.topic, content)

class LocalMessagePublisher(SpintopMessagePublisher):
    def __init__(self, local_env):
        self._local_subscribers = defaultdict(list)
        self._env = local_env

    def subscribe(self, topic, callback):
        self._local_subscribers[topic].append(callback)

    def publish(self, topic, message):
        self._publish(topic, message)
        self._notify_local(topic, message)

    def prepare_message(self, message):
        message.env = self._env.freeze_database_access_only()
        super().prepare_message(message)

    def _notify_local(self, topic, message):
        for subscriber in self._local_subscribers[topic]:
            subscriber(message)

    def _publish(self, topic, message):
        pass

class NoopMessagePublisher(SpintopMessagePublisher):
    
    def supports_publish(self):
        return False

    def supports_subscribe(self):
        return False