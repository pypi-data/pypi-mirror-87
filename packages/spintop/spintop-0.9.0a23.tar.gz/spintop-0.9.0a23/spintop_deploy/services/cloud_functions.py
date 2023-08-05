import base64
import os


from contextlib import contextmanager

from spintop_deploy.logs import _logger

from .storage import GCSFileReference
from .pub_sub import get_encoder

logger = _logger('worker-handler')

@contextmanager
def cloud_functions_context(event, context):
    try:
        logger.info(
            'This Function was triggered by '
            f'message ID {context.event_id} of type {context.event_type} '
            f'published at {context.timestamp}'
        )
        os.environ['SPINTOP_DA_UUID'] = context.event_id
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

def pub_sub_handler_factory(callback):
    def process_message(event, context):
        """Background Cloud Function to be triggered by Pub/Sub.
        Args:
            event (dict):  The dictionary with data specific to this type of
            event. The `data` field contains the PubsubMessage message. The
            `attributes` field will contain custom attributes if there are any.
            context (google.cloud.functions.Context): The Cloud Functions event
            metadata. The `event_id` field contains the Pub/Sub message ID. The
            `timestamp` field contains the publish time.
        """
        with cloud_functions_context(event, context):
            raw_bytes = base64.b64decode(event['data'])
            message = get_encoder().decode(raw_bytes)
            callback(message)
    
    return process_message

def gcs_finalize_handler_factory(callback, download_file=False):

    def process_file(event, context):
        """Background Cloud Function to be triggered by Cloud Storage.
        This generic function logs relevant data when a file is changed.

        Args:
            event (dict): The Cloud Functions event payload.
            context (google.cloud.functions.Context): Metadata of triggering event.
        Returns:
            None; the output is written to Stackdriver Logging
        """
        
        # print('Event ID: {}'.format(context.event_id))
        # print('Event type: {}'.format(context.event_type))
        # print('Bucket: {}'.format(data['bucket']))
        # print('File: {}'.format(data['name']))
        # print('Metageneration: {}'.format(data['metageneration']))
        # print('Created: {}'.format(data['timeCreated']))
        # print('Updated: {}'.format(data['updated']))


        with cloud_functions_context(event, context):
            file_ref = GCSFileReference(name=event['name'], bucket=event['bucket'])
            if download_file:
                file_ref = file_ref.download_temp()
            callback(file_ref)
    
    return process_file

class HandlerRouter():
    def __init__(self):
        self.on_gcs_finalize = None
        self.on_gcs_delete = None
        self.on_pub_sub_publish = None

    def handler_factory(self):
        ROUTES = {
            'google.pubsub.topic.publish': self._handle_pub_sub_publish,
            'google.storage.object.finalize': self._handle_gcs_finalize
        }

        def _process(event, context):
            with cloud_functions_context(event, context):
                route = ROUTES.get(context.event_type, None)
                if not route:
                    raise NotImplementedError(f'HandlerRouter does not support {context.event_type}')
                route(event, context)

        return _process

    def register_on_gcs_finalize(self, fn):
        self.on_gcs_finalize = fn
        return fn

    def register_on_gcs_delete(self, fn):
        self.on_gcs_delete = fn
        return fn

    def register_on_pub_sub_publish(self, fn):
        self.on_pub_sub_publish = fn
        return fn

    def _handle_gcs_finalize(self, event, context):
        return self._handle_file(
            filename=event['name'], 
            bucket_name=event['bucket'], 
            handler_name='on_gcs_finalize'
        )

    def _handle_file(self, filename, bucket_name, handler_name):
        handler = getattr(self, handler_name, None)
        if not handler:
            logger.info(f'Handler {handler_name} not implemented.')
        else:
            file_ref = GCSFileReference(name=filename, bucket=bucket_name)
            return handler(file_ref)
    
    def _handle_pub_sub_publish(self, event, context):
        raw_bytes = base64.b64decode(event['data'])
        attributes = event.get('attributes', {})

        message = get_encoder().decode(raw_bytes)
        message_kind = message.get('kind', None)

        gcs_event_type = attributes.get('eventType', None)
        if message_kind and message_kind == 'storage#object':
            if gcs_event_type == 'OBJECT_FINALIZE':
                return self._handle_file(
                    filename=message['name'], 
                    bucket_name=message['bucket'], 
                    handler_name='on_gcs_finalize'
                )
            elif gcs_event_type == 'OBJECT_DELETE':
                return self._handle_file(
                    filename=message['name'], 
                    bucket_name=message['bucket'], 
                    handler_name='on_gcs_delete'
                )
            else:
                logger.info(f'GCS notification of type {gcs_event_type!r} not handled')
        else:
            handler = self.on_pub_sub_publish
            if not handler:
                raise NotImplementedError('Handler @register_on_pub_sub_publish not implemented.')
            return handler(message)