import json

from flask.json import JSONEncoder as FlaskEncoder

from google.cloud import pubsub
from google.api_core.exceptions import NotFound, AlreadyExists

from spintop.models import get_json_serializer
from spintop.messages import SpintopMessagePublisher

from spintop.utils.encoding import JSONEncoder

def get_encoder():
    return JSONEncoder(encoder_cls=FlaskEncoder, sort_keys=True)

class GCPPubSub(SpintopMessagePublisher):
    def __init__(self, project_id):

        self.project_id = project_id
        self.publisher = pubsub.PublisherClient()
        self.encoder = get_encoder()

    def create_topic(self, topic_name):
        topic_path = self.topic_path(topic_name)
        self.publisher.create_topic(topic_path)

    def topic_path(self, topic_name):
        return self.publisher.topic_path(self.project_id, topic_name)

    def try_create_topic(self, topic_name):
        try:
            self.create_topic(topic_name)
        except AlreadyExists:
            pass

    def publish(self, topic_name, data, origin='spintop-api', auto_create=True):

        data_bytes = self.encoder.encode(data)

        topic_path = self.publisher.topic_path(self.project_id, topic_name)

        future = self.publisher.publish(
            topic_path, data_bytes, origin=origin
        )
        try:
            return future.result()
        except NotFound:
            if auto_create:
                self.create_topic(topic_name)
                return self.publish(topic_name, data, origin=origin, auto_create=False)
            else:
                raise
    
    def create_subscription(self, subscription_name, topic_name):
        subscriber = pubsub.SubscriberClient()
        subscription_path = subscriber.subscription_path(
            self.project_id, subscription_name
        )
        topic_path = self.publisher.topic_path(self.project_id, topic_name)
        subscriber.create_subscription(name=subscription_path, topic=topic_path)

    def try_create_subscription(self, subscription_name, topic_name):
        try:
            self.create_subscription(subscription_name, topic_name)
        except AlreadyExists:
            pass

    def pull_subscription(self, subscription_name, callback, max_messages_at_a_time=1):
        subscriber = pubsub.SubscriberClient()
        subscription_path = subscriber.subscription_path(
            self.project_id, subscription_name
        )
        
        def callback_wrapper(encoded_message):
            message = self.encoder.decode(encoded_message.data)
            callback(message)
            encoded_message.ack()

        flow_control = pubsub.types.FlowControl(max_messages=max_messages_at_a_time)
        streaming_pull_future = subscriber.subscribe(
            subscription_path, callback=callback_wrapper, flow_control=flow_control
        )
        # try:
        # When `timeout` is not set, result() will block indefinitely,
        # unless an exception is encountered first.
        streaming_pull_future.result(timeout=100)
        # except:  # noqa
        #     streaming_pull_future.cancel()
        #     raise
