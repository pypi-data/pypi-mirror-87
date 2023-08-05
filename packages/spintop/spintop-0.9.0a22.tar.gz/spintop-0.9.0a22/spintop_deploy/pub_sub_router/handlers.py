import prefect
from prefect import case, task


from .messages import (
    GCS_FINALIZE, 
    GCS_DELETE, 
    GCSFileReferenceMessage, 
    BigQueryAuditLogMessage
)

def create_any_event(data=None, attributes=None):
    return dict(
        attributes=attributes,
        data=data
    )

class Handler(object):
    def __init__(self, callback):
        self.callback = callback

    @classmethod
    def task(cls, **task_kwargs):
        def _decorator(fn):
            obj = cls(fn)
            return prefect.tasks.core.function.FunctionTask(fn=obj._run_prefect, **task_kwargs)
        return _decorator

    def _run_prefect(self, message):
        handler_message = self.filter(message)
        if not handler_message:
            raise prefect.engine.signals.SKIP(f'Message filtered by handler {self.__class__.__name__}')
        else:
            self.handle(handler_message)

    def __call__(self, message):
        handler_message = self.filter(message)
        if handler_message:
            handler.handle(handler_message)

    def filter(self, message):
        return message

    def handle(self, message):
        return self.callback(message)

    def __repr__(self):
        return f'{self.__class__.__name__}(callback={self.callback!r})'

class GCSFileChangeHandler(Handler):
    @staticmethod
    def create_event(bucket, name, event_type):
        accepted_event_types = [GCS_FINALIZE, GCS_DELETE]

        if event_type not in accepted_event_types:
            raise ValueError(f'event_type must be either one of {accepted_event_types!r}')

        return create_any_event(
            attributes=dict(
                objectId=name,
                bucketId=bucket,
                eventType=event_type
            )
        )

    def filter(self, message):
        # This returns None if incompatible.
        return GCSFileReferenceMessage.from_message(message)


class BigQueryJobHandler(Handler):

    def filter(self, message):
        # This returns None if incompatible.
        return BigQueryAuditLogMessage.from_message(message)
