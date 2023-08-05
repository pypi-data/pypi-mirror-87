from contextlib import contextmanager

from marshmallow import ValidationError

from spintop.generators import Generator

from spintop.models import (
    PersistenceRecord,
    PersistenceIDRecord,
    SerializedPersistenceRecord,
    Query,
    FieldsOf
)

from spintop.utils import AnonymousGetRecursive


from ..logs import _logger
from ..errors import SpintopException, spintop_warn
from ..messages import NoopMessagePublisher, PersistenceRecordsUpdateMessage

logger = _logger('persistence')

class MissingMapper(SpintopException):
    def __init__(self, cls):
        super().__init__("Mapper for class {!r} is mandatory.".format(cls))

class NoMapperForObject(SpintopException):
    def __init__(self, obj, mappers):
        super(NoMapperForObject, self).__init__(
            'There are no known mapper able to interact with obj {!r} of class {}. Declared mappers are: {}'.format(
                obj,
                obj.__class__,
                [cls.__name__ for cls in mappers]
            )
        )
        
class DuplicateMapperClassName(SpintopException):
    def __init__(self, objcls):
        super(DuplicateMapperClassName, self).__init__(
            'The name of the class {} is duplicate. The class name linked to a mapper must be unique.'.format(
                objcls,
            )
        )

class RecordNotFound(SpintopException):
    def __init__(self, uuid):
        super().__init__(f'Record with UUID {uuid!r} not found.')

class ManyRecordFound(SpintopException):
    def __init__(self, uuid, count):
        super().__init__(f'{count} Records where found with UUID {uuid!r}, but only one was expected.')

index_fields = FieldsOf(PersistenceIDRecord)

class PersistenceFacade(object):
    logger = logger
    def __init__(self, serializer, messages=None):
        self.serializer = serializer

        if messages is None:
            # Will discard all messages
            messages = NoopMessagePublisher()

        self.messages = messages

    @classmethod
    def from_env(cls, uri, database_name, env=None):
        raise NotImplementedError()

    @property
    def update_message(self):
        return self.messages.records_update

    def _publish_records_update(self, records):
        message = PersistenceRecordsUpdateMessage.create(
            updated_ids=[record.index for record in records]
        )
        self.update_message.publish(message)

    def _publish_update_all(self):
        spintop_warn('Current update all deletes and re-creates all tests instead of targeting deleted uuids. This is very inefficient.')
        self.update_message.publish(PersistenceRecordsUpdateMessage.create(
            update_all=True
        ))

    def serialize_barrier(self, raw_records, validate=True):
        records = self.serializer.serialize_barrier(raw_records, validate=validate)
        if records and isinstance(records[0], dict):
            return [SerializedPersistenceRecord(record) for record in records]
        else:
            return records

    def create(self, records, validate=True):
        serialized_records = self.serialize_barrier(records, validate=validate)
        ret_val = self._create(serialized_records)
        self._publish_records_update(serialized_records)
        return ret_val

    def _create(self, records):
        raise NotImplementedError()
        
    def retrieve(self, query=None, deserialize=True, limit_range=None, with_data=True):
        if query is None: query = Query()
        records = self._retrieve(query, limit_range=limit_range, with_data=with_data)
        if deserialize:
            records = list(r.as_dict() for r in records)
            yield from self.serializer.schema(many=True, partial=not with_data).load(records)
        else:
            yield from records

    def _retrieve(self, query, limit_range=None, with_data=True):
        """Should return a generator of dictionnaries of the records."""
        raise NotImplementedError()
        
    def retrieve_one(self, uuid, deserialize=True):
        records = self.retrieve(Query(index_fields.uuid == uuid), deserialize=deserialize)
        records = list(records)

        count = len(records)
        if count < 1:
            raise RecordNotFound(uuid)
        elif count > 1:
            raise ManyRecordFound(uuid, count)
        else:
            return records[0]
    
    def count(self, query=None):
        if query is None: query = Query()
        return self._count(query)
    
    def _count(self, query):
        raise NotImplementedError()

    def update(self, records, validate=True):
        serialized_records = self.serialize_barrier(records, validate=validate)
        ret_val = self._update(serialized_records)
        self._publish_records_update(serialized_records)
        return ret_val

    def _update(self, records):
        raise NotImplementedError()
    
    def delete(self, query=None):
        if query is None: query = Query()

        # Needs list() to force retrieval before deletion.
        affected_records = list(self._retrieve(query, with_data=False))
        ret_val = self._delete(query)

        for record in affected_records:
            # We retrieved them before deletion, make sure to set the flag to True.
            index_fields.is_deleted.set_value(record.index, True)
            
        self._publish_records_update(affected_records)
        return ret_val

    def _delete(self, query=None):
        raise NotImplementedError()
    
    def create_records_generator(self):
        return PersistenceGenerator(self)

    @contextmanager
    def temporary_create(self, records):
        uuids = [record.uuid for record in records]
        try:
            self.create(records)
            yield uuids
        finally:
            self.delete(Query(index_fields.uuid <= uuids))

class NotImplementedPersistenceFacade(PersistenceFacade):
    def __init__(self, **unused):
        super().__init__(None)
        
def create_mapper_name_index(mappers):
    mappers_name_index = {}
    for mapped_cls, mapper in mappers.items():
        name = mapped_cls.__name__
        if name in mappers_name_index:
            raise DuplicateMapperClassName(mapped_cls)
        mappers_name_index[name] = mapper
    return mappers_name_index
    
class PersistenceGenerator(Generator):
    def __init__(self, facade):
        super().__init__()
        self.facade = facade
    
    def __call__(self, *args, **kwargs):
        return self.facade.retrieve(*args, **kwargs)

class Mapper(object):
    def init(self):
        pass