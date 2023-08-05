from sqlalchemy import Column, Boolean, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON, JSONB, UUID
from sqlalchemy.ext.declarative import declarative_base

from spintop.models import PersistenceIDRecord, SerializedPersistenceRecord
from spintop.models.serialization import TYPE_KEY

Base = declarative_base()

fields = PersistenceIDRecord.fields()

# Native table fields. The rest is in the 'index' JSONB column of the table

# Those are replicated in the serialized version as-is
writeable_top_level_fields = { fields.uuid, fields.is_deleted }

# Those are simply indexed when the index data changes.
# Datetime is omitted since it would require serialization/deserialization from postgresql TIMESTAMP
top_level_fields = writeable_top_level_fields | { fields.start_datetime }

class DataBlob(Base):
    __tablename__ = 'data_blobs'
    blob_id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    _group = Column(String, primary_key=True, nullable=True)
    data = Column(JSON)

class RecordIndex(Base):
    __tablename__ = 'records_index'
    # top level fields
    uuid = Column(String, primary_key=True)
    is_deleted = Column(Boolean)
    start_datetime = Column(DateTime(timezone=True))
    #

    _group = Column(String, primary_key=True, nullable=True)
    _type = Column(String)

    index = Column(JSONB)
    data_blob_id = Column(UUID(as_uuid=True), ForeignKey(DataBlob.blob_id, ondelete='SET NULL'), nullable=True)

    data_blob = relationship(DataBlob)

    @classmethod
    def create(cls, record, _group=None, data_blob_id=None):
        return cls(
            index=record.index, 
            _type=record.type_,
            _group=_group,
            data_blob_id=data_blob_id,
            **{field.name_: field.get_value(record.index) for field in top_level_fields}
        )

    def to_serialized_record(self, with_data=True):
        content = {
            TYPE_KEY: self._type,
            'index': self.index
        }

        for field in writeable_top_level_fields:
            # Source of truth are the top level fields.
            # Replicate them inside the index, but serialize them first
            field.set_value(content['index'], getattr(self, field.name_))

        if with_data:
            content['data'] = self.data_blob.data
        return SerializedPersistenceRecord(content)
