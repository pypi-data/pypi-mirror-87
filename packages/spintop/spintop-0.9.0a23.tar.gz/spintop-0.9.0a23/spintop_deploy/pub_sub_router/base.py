import logging

from collections.abc import Mapping
from contextlib import contextmanager

from prefect import task

from .messages import Message, encode_data

logger = logging.getLogger(__name__)

@contextmanager
def cloud_functions_context(event, context):
    try:
        if context:
            logger.info(
                'This Function was triggered by '
                f'message ID {context.event_id} of type {context.event_type} '
                f'published at {context.timestamp}'
            )
        else:
            logger.info('No context information surrounding function trigger.')
        yield
    except: # pylint: disable=bare-except
        logger.exception('Exception occured', exc_info=True)
        try_report_active_exc()

def try_report_active_exc():
    try:
        from google.cloud import error_reporting
        client = error_reporting.Client()
        client.report_exception()
    except: # pylint: disable=bare-except
        logger.warning('Unable to report to google error reporting', exc_info=True)

class PubSubRouter():
    def __init__(self, handlers=None):
        if handlers is None:
            handlers = []
        self.handlers = handlers

    def cloud_functions_handler(self):
        return self._handle_cloud_functions

    def _handle_cloud_functions(self, event, context):
        with cloud_functions_context(event, context):
            print(f'event={event}')
            message = Message(event=event, context=context)
            self.handle(message)

    def pub_sub_handler(self):
        return self._handle_pub_sub

    def _handle_pub_sub(self, pub_sub_message):
        message = Message(event={'data': pub_sub_message.data}, context=None)
        self.handle(message)

    def request_handler(self):
        return self._handle_request

    def _handle_request(self, request_content):
        message_event = request_content.pop('message')
        message = Message(event=message_event, context=request_content)
        self.handle(message)

    def handle(self, message):
        handled = False
        for handler in self.handlers:
            handler_message = handler.filter(message)
            if handler_message:
                print(f'Using handler {handler!r}')
                handled = True
                break_handling = handler.handle(handler_message)
                if break_handling:
                    break
        
        if not handled:
            print(f'No handlers for message')


class PubSubTrigger(object):
    def __init__(self, topic):
        self.topic = topic
        from google.cloud import pubsub
        self._client = pubsub.PublisherClient() 

    @property
    def client(self):
        return self._client

    def trigger(self, message):
        print(f'Triggering {message!r}')
        return self.trigger_event(message.event)

    def trigger_event(self, event):
        event = encode_event(event)
        data_encoded = event['data']
        attributes = event['attributes']
        print(f'Publishing data={data_encoded!r}, attributes={attributes!r}')
        self.client.publish(self.topic, data_encoded, **attributes)

def encode_event(event):
    data = event.get('data', {})
    attributes = event.get('attributes', {})
    return dict(
        data=encode_data(data),
        attributes=attributes
    )
    
