""" Base models that allow persistency and indexing using the spintop.persistence modules.
"""
from datetime import datetime
from collections import OrderedDict
from typing import List, Dict, Optional, Any, NamedTuple

from .base import BaseDataClass, model_property, model_attribute, DefaultPrimitiveView
from .common import OutcomeData, DutIDRecord, VersionIDRecord
from .serialization import SerializedWrapper, TYPE_KEY, ValidationError, cls_subclasses, cls_of_serialized
from .queries import BaseQuery
from .meta import FieldsOf
from .view import DataClassPrimitiveView

from spintop.utils import utcnow_aware, is_aware, dict_ops, is_valid_py_identifier, isnan

def validate_tags_are_py_identifers(tags):
    for key in tags:
        if not is_valid_py_identifier(key):
            raise ValidationError(f'{key!r} is not a valid python identifier.')

def create_uuid():
    return uuid4()

def uuid_to_slug(uuidstring):
    try:
        uuid = UUID(uuidstring)
    except AttributeError:
        uuid = uuidstring
    
    return urlsafe_b64encode(uuid.bytes).rstrip(b'=').decode('ascii')

def uuid_generator(*parts):
    parts_str = []

    for part in parts:
        if hasattr(part, 'strftime'):
            # datetime
            parts_str.append(part.strftime("%Y%m%d-%H%M%S-%f"))
        else:
            parts_str.append(str(part))

    if not parts_str:
        # Not enough info for unique id. Generate one.
        return uuid_to_slug(create_uuid())
    else:
        return '.'.join(parts_str)

class PersistenceIDRecord(BaseDataClass):
    
    fields_docs_ = dict(
        uuid="""
    The UUID of this record. No explicit checks are made to validate the uniqueness of this ID.
    It should be defined using the start_datetime and other pertinent fields.
        """,
        is_deleted="""
    Reserved for future use.
        """,
        tags="""
    A dictionnary of user defined tags to associated with this record.
        """,
        start_datetime="""
    A datetime object that defines the START time of this record.
        """
    )

    uuid: str
    is_deleted: bool = False
    tags: Dict[str, Optional[Any]] = model_attribute(dict, validators=[validate_tags_are_py_identifers])
    start_datetime: datetime = utcnow_aware

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.start_datetime and not is_aware(self.start_datetime):
            raise ValueError('Please provide a tz-aware datetime.')


class PersistenceRecord(BaseDataClass):
    # Common to all
    uuid: str = model_property(fget=lambda record: record.index.uuid)

    # Same attributes, type should be changed by sub classes.
    index: PersistenceIDRecord = None
    data: BaseDataClass = None

class SerializedPersistenceRecord(SerializedWrapper):
    pass

class ProcessStepIDRecord(PersistenceIDRecord):
    step: VersionIDRecord = None
    station: VersionIDRecord = None
    dut: DutIDRecord = DutIDRecord
    operator: str = None
    stage: str = 'prod'
    duration: float = None
    outcome: OutcomeData = None
    
    def __post_init__(self):
        super().__post_init__()
        self.dut = DutIDRecord.create(self.dut)
        
        if self.step is not None:
            self.step = VersionIDRecord.create(self.step)
        
        if self.station is not None:
            self.station = VersionIDRecord.create(self.station)

        if self.outcome is not None:
            self.outcome = OutcomeData.create(self.outcome)
            
        for key, value in self.tags.items():
            self.add_tag(key, value)

        if self.uuid is None:
            self.uuid = uuid_generator(self.step, self.start_datetime, self.dut)
            

    def add_tag(self, key, value=True):
        self.tags[key] = tag_value_sanitizer(value)
        
    def remove_tag(self, key):
        del self.tags[key]
        
def tag_value_sanitizer(value):
    if isinstance(value, float) and isnan(value):
        # NaN to None.
        value = None

    return value

class ProcessStepRecord(PersistenceRecord):
    index: ProcessStepIDRecord = None

class QualityStepIDRecord(ProcessStepIDRecord):
    """Outcome now included in ProcessStepIDRecord"""

class QualityStepRecord(ProcessStepRecord):
    """Outcome now included in ProcessStepIDRecord"""

class AssemblyStepIDRecord(PersistenceIDRecord):
    duts: List[DutIDRecord] = list

    def __post_init__(self):
        super().__post_init__()
        self.duts = [DutIDRecord.create(dut) for dut in self.duts]

class AssemblyStepRecord(PersistenceRecord):
    index: AssemblyStepIDRecord = None

index_fields = PersistenceIDRecord.fields()

def all_query_fields_dict():
    all_fields = list(PersistenceIDRecord.fields())

    for subcls in cls_subclasses(PersistenceIDRecord):
        all_fields += list(subcls.fields())

    return {field.field_name_: field for field in all_fields}

class PersistenceRecordCollection(BaseDataClass):
    records: List[PersistenceRecord] = list

    def __init__(self, records=None):
        records = list(records) if records else []
        super().__init__(records=sorted(records, key=lambda record: index_fields.uuid.get_value(record.index)))
    
    @property
    def collector(self):
        return self.add_record

    def add_record(self, record):
        self.records.append(record)
        
    def apply(self, *fns):
        for record in self.iter_records():
            for fn in fns:
                fn(record)
                
    def iter_records(self):
        for record in self.records:
            yield record
                
    def count_unique(self, key=lambda record: record.uuid):
        occurances = set()
        self.apply(lambda record: occurances.add(key(record)))
        return len(occurances)
            
    def sort(self, key=lambda record: record.index.start_datetime):
        self.records.sort(key=key)
        
    def __eq__(self, other):
        return self.records == other.records

class Query(BaseQuery):
    
    def default_parts(self):
        yield index_fields.is_deleted == False

    @classmethod
    def from_q_string(cls, q_string):
        return Query(eval(q_string, {}, all_query_fields_dict()))


class PersistenceRecordView(object):
    data_prefix = ('data',)
    index_prefix = ()
    default_view = DefaultPrimitiveView()
    
    def __init__(self, data_view=None, include_index=True, include_data=True, data_prefix=None, index_prefix=None):
        self.include_index = include_index
        self.include_data = include_data

        if data_view:
            self.data_view = DataClassPrimitiveView(data_view)
        else:
            self.data_view = None

        if data_prefix is not None:
            self.data_prefix = data_prefix
        
        if index_prefix is not None:
            self.index_prefix = index_prefix

    def apply(self, record, flatten_dict=True):
        result = OrderedDict()
        
        if self.include_index:
            index_data = self.apply_index(record, flatten_dict=flatten_dict, key_prefix=self.index_prefix)
            dict_ops.update(result, index_data)
        
        if self.data_view:
            data = self.apply_data(record, flatten_dict=flatten_dict, key_prefix=self.data_prefix)
            dict_ops.update(result, data)
        
        result = dict_ops.replace_defaults(result)

        return result
    
    def apply_index(self, record, **apply_kwargs):
        return self.default_view.apply(record.index, **apply_kwargs)

    def apply_data(self, record, **apply_kwargs):
        return self.data_view.apply(record.data, **apply_kwargs)

def cls_of_record(record):
    if isinstance(record, BaseDataClass):
        return record.__class__

    if isinstance(record, SerializedPersistenceRecord):
        data = record.as_dict()
    else:
        data = record

    if data:
        return cls_of_serialized(data)
    else:
        return None