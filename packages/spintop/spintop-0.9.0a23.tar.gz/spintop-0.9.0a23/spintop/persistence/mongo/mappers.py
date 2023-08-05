
from .operations import MongoOperations, ASCENDING
from .serialization import DataClassSerializer

from spintop.models import (
    TestIDRecord,
    SpintopTestRecord,
    SpintopTestRecordBuilder,
    Query,
    FieldsOf
)


from ...logs import _logger


SIMPLE_MAPPER_DATACLASSES_COLLECTION_NAMES = {}

SIMPLE_MAPPER_DATACLASSES_INIT_FNS = {}

logger = _logger('mongo')

def register_simple_mapper(cls, collection_name):
    SIMPLE_MAPPER_DATACLASSES_COLLECTION_NAMES[cls] = collection_name
    SIMPLE_MAPPER_DATACLASSES_INIT_FNS[cls] = None
    def _register_init(fn):
        SIMPLE_MAPPER_DATACLASSES_INIT_FNS[cls] = fn
        return fn
    return _register_init

TestUUID = FieldsOf(TestIDRecord).uuid
DateTime = FieldsOf(TestIDRecord).start_datetime
Index = FieldsOf(TestIDRecord).index

# Mappers
@register_simple_mapper(TestIDRecord, 'test-features')
def init_test_record_mapper(mapper):
    test_uuid_field = TestUUID.name_
    datetime_field = DateTime.name_
    index_field = Index.name_

    mapper.ops.create_index([(test_uuid_field, ASCENDING), (index_field, ASCENDING)], unique=True)
    mapper.ops.grouped_by = test_uuid_field

def create_mappers(mongo_db, serializer=None, operations_factory=None):
    
    # Simple mappers are 1:1 with a document in a mongo collection.
    mappers = {}
    for dataclass, collection_name in SIMPLE_MAPPER_DATACLASSES_COLLECTION_NAMES.items():
        init_fn = SIMPLE_MAPPER_DATACLASSES_INIT_FNS[dataclass]
        mappers[dataclass] = simple_mongo_mapper_factory(
            mongo_db, 
            collection_name, 
            serializer=serializer,
            on_init=init_fn,
            operations_factory=operations_factory
        )
    
    return mappers

def simple_mongo_mapper_factory(mongo_db, collection_name, serializer=None, on_init=None, operations_factory=None):
    if operations_factory is None: operations_factory = MongoOperations

    ops = operations_factory(mongo_db[collection_name])
    return SimpleMongoMapper(ops, serializer=serializer, on_init=on_init, name=collection_name)


class SimpleMongoMapper(object):
    def __init__(self, ops, serializer=None, on_init=None, name="simple"):
        if serializer is None: serializer = DataClassSerializer()
        self.ops = ops
        self.dc_serializer = serializer
        self.on_init = on_init
        self.logger = logger.getChild(name)
    
    def init(self):
        if self.on_init: self.on_init(self)
    
    def create(self, serialized_dcs):
        serialized_dcs = [self.dc_serializer.serialized_to_mongo_id(dc, keep_id_if_none=False) for dc in serialized_dcs]
        
        resp = self.ops.insert_many(serialized_dcs)
        self.logger.info('Inserted %d new documents' % len(resp.inserted_ids))
        
        # ids are inserted client side into the 'serialized' dictionnary.
        # We can re-insert _ids into dataclasses.
        for dc, serialized in zip(serialized_dcs, serialized_dcs):
            dc['oid'] = serialized['_id']
            
    def count(self, query=Query()):
        return self.ops.count(query)

    def count_total(self, query=Query()):
        return self.ops.count_total(query)

    def collection_stats(self):
        return self.ops.collection_stats()

    def retrieve(self, query=Query(), limit_range=None):
        responses = self.ops.find(query, limit_range=limit_range)
        return [self.dc_serializer.serialized_from_mongo_id(dc) for dc in responses]
        
    def update(self, serialized_dcs, query_fields):
        """Non-working. Facade uses a combination of delete + create to mimick update behavior."""
        # serialized_dcs = self.dc_serializer.serialize_many(dataclasses)
        if not query_fields:
            raise ValueError('query_fields must be a non-empty list of MetaFields.')

        def obj_query(obj):
            q = {field.name_: field.value_of_serialized(obj) for field in query_fields}
            return q

        self.ops.update_many(serialized_dcs, obj_query)
        
    def delete(self, query=Query()):
        resp = self.ops.delete_many(query)
        self.logger.info('Deleted %d documents' % resp.deleted_count)