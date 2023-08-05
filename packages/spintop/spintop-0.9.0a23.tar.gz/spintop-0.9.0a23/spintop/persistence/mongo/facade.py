import os

from spintop.persistence import PersistenceFacade
from spintop.models import (
    SpintopTestRecord,
    SpintopSerializedTestRecord,
    SpintopSerializedTestRecordCollection,
    Query
)
from spintop.errors import SpintopException

from .operations import db_from_mongo_uri
from .mappers import create_mappers, simple_mongo_mapper_factory, TestIDRecord

class MongoPersistenceFacade(PersistenceFacade):
    def __init__(self, mongo_db=None, uri=None, database_name=None, serializer=None, **unused):
        
        if mongo_db is None:
            if uri is not None and database_name is not None:
                mongo_db = db_from_mongo_uri(uri, database_name)
            else:
                raise ValueError('The mongo_db or uri + database_name parameters are required.')

        self.mongo_db = mongo_db
        self.serializer = serializer
        mappers = create_mappers(mongo_db, serializer=serializer)
        self.feature_mapper = mappers[TestIDRecord]
        self._init(mappers)
        self.dc_serializer = self.feature_mapper.dc_serializer

        super().__init__(self.dc_serializer.serializer)
    
    def _init(self, mappers):
        for _, mapper in mappers.items():
            mapper.init()
        
    def _create(self, records):
        self._iter_op('create', records)
        
    def _iter_op(self, op_name, records):
        all_features = []
        for record in records:
            all_features += record.all_features

        self.logger.info('Processing {} of {} features.'.format(
                op_name, len(all_features)
            )
        )
        getattr(self.feature_mapper, op_name)(all_features)
    
    def count(self, query=None):
        if query is None:
            query = Query()
        return self.feature_mapper.count(query)
    
    def avg_obj_size(self):
        # Count is based on test records, multiple avg feature size with avg feature count
        avg_feature_count = self.feature_mapper.count_total() / self.feature_mapper.count()
        return self.feature_mapper.collection_stats().get('avgObjSize') * avg_feature_count
        
    def _retrieve(self, query=None, limit_range=None):
        """ Retrieve is responsible with returning the test_record (top level phase) associated
        with the matched features.
        """
        query = self._include_top_level_in_query(query)
        all_features = self.feature_mapper.retrieve(query, limit_range=limit_range)

        raise NotImplemented('from_features was removed. Mongo needs refactoring to work again.')
        return SpintopSerializedTestRecordCollection.from_features(all_features)

    def _include_top_level_in_query(self, query):
        if query is None:
            query = Query()
        return [query.create_top_level_query(), query]

    def _update(self, records):
        all_features = []
        test_uuids = []

        for record in records:
            all_features += record.all_features
            test_uuids += [record.test_uuid]

        self.feature_mapper.delete(Query().test_uuid_any_of(test_uuids))
        self.feature_mapper.create(all_features)
    
    def _delete(self, match_query):
        match_query = self._include_top_level_in_query(match_query)
        self.logger.info('Deleting flat records based on query: %s.' % repr(match_query))
        self.feature_mapper.delete(match_query)

    def create_mapper(self, name, **kwargs):
        return simple_mongo_mapper_factory(self.mongo_db, name, serializer=self.serializer, **kwargs)