import datetime as dt
import traceback

from spintop.utils import utcnow_aware
from spintop.models import (
    BaseDataClass,
)

from spintop.logs import _logger

logger = _logger('filehandler')

class FileHandlingContext(object):
    def __init__(self, filename, env):
        self.env = env
        self.filename = filename
        self.start_event = None

    def new_event(self, event_type):
        return SpintopFileReference(
            filename=self.filename,
            pipeline_uuid=str(self.env.uuid),
            event=SpintopFileEvent(event_type=event_type)
        )

    def __enter__(self):
        self.start_event = self.new_event('start')
    
    def __exit__(self, exc_type, exc_value, traceback):
        end_event = self.new_event('end')
        logger.info('Finalizing file handling analytics.')
        if exc_type:
            logger.warning('Error occured, sending events then reraising...')
            end_event.event.severity = 'ERROR'
            end_event.event.data = {
                'exc_type': str(exc_type),
                'exc_value': str(exc_value),
                'traceback': str(traceback)
            }
        
        self.env.analytics_factory().processed_files.update([
            self.start_event,
            end_event
        ])

class SpintopFileEvent(BaseDataClass):
    start_datetime: dt.datetime = utcnow_aware
    event_type: str = 'start'
    data: dict = dict
    severity: str = 'INFO'
    count: int = 1

class SpintopFileReference(BaseDataClass):
    filename: str
    pipeline_uuid: str
    event: SpintopFileEvent = None
