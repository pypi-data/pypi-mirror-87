import os
import uuid
from collections import OrderedDict

from spintop.persistence import PersistenceFacade
from spintop.models.persistence import (
    PersistenceIDRecord, 
    PersistenceRecord, 
    PersistenceRecordCollection
)

from spintop.models import (
    Query,
    get_json_serializer,
    FieldsOf
)

from spintop.errors import SpintopException

from .models import RecordIndex, DataBlob
from .operations import engine_from_uri, SQLOperations
from .queryset import PostgreSQLQuery

index_fields = FieldsOf(PersistenceIDRecord)

class PostgreSQLPersistenceFacade(PersistenceFacade):
    def __init__(self, sql_engine=None, uri=None, database_name='default', **unused):
        
        if sql_engine is None:
            if uri is not None:
                sql_engine = engine_from_uri(uri)
            else:
                raise ValueError('The sql_engine or uri parameter is required.')

        self.sql_ops = SQLOperations(sql_engine)
        self.serializer = get_json_serializer()
        super().__init__(self.serializer)
        self.init()
        self.group = database_name

    def init(self):
        self.sql_ops.create_tables()
        
    def _create(self, records):
        self._update(records)
    
    def add_records_to_session(self, session, records):
        # Create the data blobs
        data_blobs = [None]*len(records)
        for idx, record in enumerate(records):
            if not record.index['is_deleted']:
                data_blob = DataBlob(data=record.data, _group=self.group, blob_id=uuid.uuid4())
            data_blobs[idx] = data_blob

        session.bulk_save_objects(data_blobs)

        
        uuids_to_indices = {}
        
        for record, data_blob in zip(records, data_blobs):
            uuids_to_indices[record.uuid] = RecordIndex.create(
                record,
                _group=self.group,
                data_blob_id=data_blob.blob_id if data_blob else None
            )

        uuids = list(uuids_to_indices.keys())

        # Query these uuids, deleted or not.
        existing_query = Query(
            index_fields.uuid <= uuids, 
            index_fields.is_deleted.any_()
        )

        existing_indices = list(self._index_query_filter(session, existing_query).all())
        for record_index in existing_indices:
            # Only merge those records which already exist in the database
            session.merge(uuids_to_indices.pop(record_index.uuid))

        # Only add the records which did not exist in the database
        session.add_all(uuids_to_indices.values())

    def count(self, query=None):
        if query is None: query = Query()
        with self.sql_ops.new_session() as session:
            operation = session.query(RecordIndex).filter(*self._to_filter(query))
            return operation.count()
    
    def avg_obj_size(self):
        raise NotImplementedError()
        
    def _retrieve(self, query=None, limit_range=None, with_data=True):
        """ Retrieve is responsible with returning the test_record (top level phase) associated
        with the matched features.
        """
        with self.sql_ops.new_session() as session:
            if query is None: query = Query()
            
            operation = self._index_query_filter(session, query).order_by(RecordIndex.uuid.asc())
            
            if with_data:
                operation = operation.join(RecordIndex.data_blob)

            if limit_range:
                operation = operation.offset(limit_range[0]).limit(limit_range[1] - limit_range[0])

            yield from (record.to_serialized_record(with_data=with_data) for record in operation.all())

    def _index_query_filter(self, session, query):
        return session.query(RecordIndex).filter(*self._to_filter(query))

    def _to_filter(self, query):
        return PostgreSQLQuery(query).build_data_query(RecordIndex) + [RecordIndex._group == self.group]

    def _update(self, records):
        uuids = [record.uuid for record in records]

        with self.sql_ops.new_session() as session:
            # Delete referenced
            self._delete_query_from_session(session, Query(index_fields.uuid <= uuids))
            # Then update
            self.add_records_to_session(session, records)
            session.commit()
    
    def _delete_query_from_session(self, session, query):
        filters = self._to_filter(query)

        # Filter the datablobs by the ids referenced by indices of filters
        # Delete them.
        # The cascading effect will set the data_blob_id of indices to NULL.
        session.query(DataBlob).filter(DataBlob.blob_id == RecordIndex.data_blob_id, *filters).delete(synchronize_session=False)

        # Set the indices is_deleted = True
        session.query(RecordIndex).filter(*filters).update(
            {RecordIndex.is_deleted: True},
            synchronize_session=False
        )

    def _delete(self, match_query):
        with self.sql_ops.new_session() as session:
            self._delete_query_from_session(session, match_query)
            session.commit()
