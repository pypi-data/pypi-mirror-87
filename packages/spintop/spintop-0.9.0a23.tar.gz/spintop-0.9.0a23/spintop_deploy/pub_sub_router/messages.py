import os
import base64
import json
import tempfile

from shutil import copyfile
from binascii import Error as DecodeError
from collections.abc import Mapping

BYTES_ENCODING = 'utf-8'

def decode_data(data):
    raw_bytes = data
    # print(raw_bytes)
    # endswith = b'=' if isinstance(data, bytes) else '='
    # if data.endswith(endswith):

    try:
        raw_bytes = base64.b64decode(data)
    except DecodeError:
        pass # use raw_bytes = data
    
    try:
        string = raw_bytes.decode(BYTES_ENCODING)
    except (
            UnicodeDecodeError, # unable to decode
            AttributeError # 'str' object has no attribute 'decode'
        ):
        string = raw_bytes
    # print(string)
    try:
        return json.loads(string)
    except json.JSONDecodeError:
        return {}

def encode_data(data):
    raw_bytes = json.dumps(data).encode(BYTES_ENCODING)
    return base64.b64encode(raw_bytes)

class Message(object):
    def __init__(self, event=None, context=None, data=None):
        if event is None:
            event = {'data': data}
        self._event = event
        self._context = context
        self._data = data

    @classmethod
    def from_message(cls, other_message):
        return cls(event=other_message.event, context=other_message.context)

    @property
    def event(self):
        return self._event

    @property
    def context(self):
        return self._context

    @property
    def attributes(self):
        if self.event:
            return self.event.get('attributes', {})
        else:
            return {}

    @property
    def event_type(self):
        return self.attributes.get('eventType')

    @property
    def data(self):
        if not self._data and self.event:
            # lazy load
            data = self.event.get('data')
            if isinstance(data, Mapping):
                # probably already decoded.
                self._data = data
            else:
                self._data = decode_data(data)

        return self._data

    def __repr__(self):
        return f'{self.__class__.__name__}(event={self.event},context={self.context})'

GCS_FINALIZE = 'OBJECT_FINALIZE'
GCS_DELETE = 'OBJECT_DELETE'

class GCSFileReferenceMessage(Message):

    @classmethod
    def from_message(cls, other_message):
        if other_message.event_type not in [GCS_FINALIZE, GCS_DELETE]:
            return None
        else:
            return super().from_message(other_message)

    @property
    def name(self):
        return self.attributes['objectId']

    @property
    def bucket(self):
        return self.attributes.get('bucketId', '__local__')

    def is_finalized(self):
        return self.event_type == GCS_FINALIZE

    def is_deleted(self):
        return self.event_type == GCS_DELETE

    def download_to_filename(self, filename):
        from google.cloud import storage
        storage_client = storage.Client()

        bucket = storage_client.bucket(self.bucket)
        blob = bucket.blob(self.name)
        blob.download_to_filename(filename)
    
    def download_temp(self):
        name = self.name
        if os.path.isabs(name):
            # Abs path. Use only filename for temp location or abspath will be used.
            _, name = os.path.split(name)
        
        filename = os.path.join(tempfile.gettempdir(), self.bucket, name)

        folder, _ = os.path.split(filename)
        os.makedirs(folder, exist_ok=True)
        
        self.download_to_filename(filename)
        return filename

class FileReferenceMessage(GCSFileReferenceMessage):
    def download_to_filename(self, filename):
        copyfile(self.name, filename)

class LogMessage(Message):

    @property
    def payload(self):
        return self.data.get('protoPayload', {})

    @property
    def service_name(self):
        return self.payload.get('serviceName')

    @property
    def service_data(self):
        return self.payload.get('serviceData')


class BigQueryAuditLogMessage(LogMessage):

    @classmethod
    def from_message(cls, other_message):
        message = super().from_message(other_message)
        if message.service_name == 'bigquery.googleapis.com':
            return message
        else:
            return None

    @property
    def bq_event_data(self):
        return self.service_data.get('jobCompletedEvent', {})

    @property
    def bq_job(self):
        return self.bq_event_data.get('job', {})

    @property
    def bq_job_config(self):
        return self.bq_job.get('jobConfiguration', {})

    @property
    def query_config(self):
        return self.bq_job_config.get('query', {})

    @property
    def job_status(self):
        return self.bq_job_config.get('jobStatus', {})

    @property
    def project_id(self):
        return self.query_config.get('destinationTable', {}).get('projectId')

    @property
    def dataset_id(self):
        return self.query_config.get('destinationTable', {}).get('datasetId')

    @property
    def table_id(self):
        return self.query_config.get('destinationTable', {}).get('tableId')

    @property
    def job_state(self):
        return self.job_status.get('state')

    def is_query_job_completed(self):
        return self.bq_event_data.get('eventName') == 'query_job_completed'
