
from itertools import chain

from collections import OrderedDict, defaultdict
from collections.abc import Mapping
from typing import NamedTuple, List, Dict, Any, Optional

from marshmallow import Schema, post_dump, pre_load

from spintop.logs import deprecated
from spintop.utils import GetRecursive, GetRecursiveMixin, dict_ops

from ..serialization import (
    is_serialized_type_of,
    type_of
)

from ..view import DataClassPrimitiveView, ComplexPrimitiveView
from ..meta import FieldsOf

from ..persistence import QualityStepRecord, PersistenceRecordCollection, PersistenceRecordView

from ._base import (
    model_property,
    BaseDataClass,
    TestIDRecord,
    FeatureRecord,
    compute_stats
)

SUPPORT_MISSING_TOP_LEVEL_RECORD = False

def normalize_features_len(dict_array):
    new_dict = {}
    max_column_key_len = max([len(key) for key in dict_array])
    for key, value in dict_array.items():
        if len(key) < max_column_key_len:
            key = key + ('',)*(max_column_key_len - len(key))
        new_dict[key] = value
    return new_dict

class TestDataRecord(BaseDataClass):
    features: List[FeatureRecord] = list

class SpintopTestRecord(QualityStepRecord):

     # QualityStepRecord interface
    index: TestIDRecord = None
    data: TestDataRecord = TestDataRecord

    ## Alias properties ##

    @property
    def summary(self) -> TestIDRecord:
        return self.index
        
    @property
    def test_id(self):
        return self.index

    @test_id.setter
    def test_id(self, value):
        self.index = value
    
    @property
    def features(self) -> List[FeatureRecord]:
        return self.data.features

    @features.setter
    def features(self, features):
        self._broadcast_test_id(features)
        self.data.features = tuple(sorted(features, key=lambda feature: feature.index))

    ## Other properties ##

    @property
    def all_features(self):
        return tuple(self.features)

    def compute_stats(self):
        if not self.summary.feature_count:
            compute_stats(self.all_features)

    @property
    def test_record(self):
        deprecated('Please use the `summary` attribute instead.')
        return self.summary

    @property
    def test_uuid(self):
        return self.test_id.uuid
    
    def __hash__(self):
        return hash(self.test_uuid)

    def __eq__(self, other):
        return self.summary == other.summary and self.features == other.features
    
    def __repr__(self):
        return '{}(summary={!r}, features=[...]*{})'.format(self.__class__.__name__, self.summary, len(self.features))

    def remove_duplicate_features(self):
        feature_names = set()
        features = []
        for feature in self.features:
            if feature.name in feature_names:
                continue
            else:
                features.append(feature)
                feature_names.add(feature.name)
        
        self.features = features
    
    def _broadcast_test_id(self, features):
        """Uses the top level test_id and sets it for all features, ensuring
        that all features have the same TestIDRecord reference."""
        for feature in features:
            feature.test_id = self.test_id
    
    def reindex(self):
        for index, feature in enumerate(self.features):
            feature.index = index

    def normalize_outcomes(self):
        parents = tuple()
        last_feature = None
        for feature in self.all_features:
            while feature.depth > len(parents):
                if last_feature.name not in feature.ancestors:
                    raise Exception('Unable to normalize outcomes: feature order does not match ancestors. {!r} should be in ancestors: {!r}'.format(
                        last_feature.name,
                        feature.ancestors
                    )) 
                parents = parents + (last_feature,)

            if feature.depth < len(parents):
                parents = parents[:feature.depth]

            outcome = feature.outcome

            for parent in reversed(parents):
                outcome.impose_upon(parent.outcome)
                outcome = parent.outcome

            last_feature = feature

            
    def fill_missing_from_source(self, fill_source, on_fill=None):
        max_current_feature_index = max(self.features, key=lambda f: f.index)
        new_features_len = len(fill_source)
        
        assert new_features_len >= max_current_feature_index.index, "Fill source must be same length or bigger than this test_record max index."
        
        new_features = [None]*new_features_len
        
        if on_fill is None:
            on_fill = lambda obj: obj.copy()
            
        def fill_range(start, end):
            for i in range(start, end):
                new_features[i] = on_fill(fill_source[i])
        
        current_index = 0
        for feature in sorted(self.features, key=lambda f: f.index):
            fill_range(current_index, feature.index)
            new_features[feature.index] = feature # Keep this feature
            current_index = feature.index + 1
        
        fill_range(current_index, new_features_len) # Fill end
        
        self.features = new_features
                
    def find_feature(self, condition, start_index=0):
        try:
            return next(feat for feat in self.all_features[start_index:] if condition(feat))
        except StopIteration:
            raise ValueError('No feature matched condition.')
    
    def add_tag(self, key, value=True):
        self.test_id.add_tag(key, value=value)
        
    def remove_tag(self, key):
        self.test_id.remove_tag(key)

spintop_test_record_features = FieldsOf(SpintopTestRecord).features
spintop_test_record_test_id = FieldsOf(SpintopTestRecord).index

class SpintopTestRecordCollection(PersistenceRecordCollection):
    records: List[SpintopTestRecord] = list

    @property
    def test_uuids(self):
        return [record.uuid for record in self.records]
            
    def are_records_unique(self):
        test_uuids = self.test_uuids
        return len(test_uuids) == len(set(test_uuids))
        
    def avg_feature_count(self):
        feature_counts = [len(record.features) for record in self.iter_records()]
        return sum(feature_counts)/len(feature_counts)

class SpintopTestRecordView(PersistenceRecordView):
    # data_prefix = ('features', lambda feat: type_of(feat), lambda feat: feat.complete_name)
    data_prefix = ('features',)
    
    def apply_data(self, record, **apply_kwargs):
        data = OrderedDict()
        for feature in record.data.features:
            feature_data = self.data_view.apply(feature, **apply_kwargs)
            dict_ops.update(data, feature_data)

        return data

class SpintopTestRecordBuilder(NamedTuple):
    summary: TestIDRecord
    features: List[FeatureRecord]
    
    def build(self):
        record = SpintopTestRecord(index=self.summary, features=sorted([self.summary] + self.features, key=lambda feature: feature.index))
        record.compute_stats()
        return record

class SpintopSerializedTestRecord(object):
    def __init__(self, serialized_record=None):
        if not serialized_record: serialized_record = self.create_empty_serialized_record()
        self._record = serialized_record

        if not self.features:
            self.features = []

    def create_empty_serialized_record(self):
        record = SpintopTestRecord()
        schema = SpintopTestRecord.get_schema()
        return schema().dump(record)

    # @property
    # def summary(self):
    #     return spintop_test_record_summary.get_value(self._record)

    # @summary.setter
    # def summary(self, value):
    #     spintop_test_record_summary.set_value(self._record, value)

    @property
    def test_record(self):
        deprecated('Please use the `summary` attribute instead.')
        return self.summary

    @property
    def features(self):
        return spintop_test_record_features.get_value(self._record)

    @features.setter
    def features(self, value):
        spintop_test_record_features.set_value(self._record, value)

    @property
    def test_id(self):
        return spintop_test_record_test_id.get_value(self._record)

    @property
    def test_uuid(self):
        return self.test_id['uuid']

    @property
    def all_features(self):
        return (self.summary,) + tuple(self.features)

    def as_dict(self):
        return self._record

    def deserialize(self, serializer):
        builder = SpintopTestRecordBuilder(
            summary=serializer.deserialize(self.summary), 
            features=tuple(serializer.deserialize(feat) for feat in self.features)
        )
        return builder.build()

    def __repr__(self):
        return '{}(summary={!r}, features=[...]*{})'.format(self.__class__.__name__, self.summary, len(self.features))

    def __eq__(self, other):
        return self._record == other._record

class SpintopSerializedTestRecordCollection(object):
    records: List[SpintopSerializedTestRecord]

    def __init__(self, records:SpintopSerializedTestRecord = None):
        self.records = [
            SpintopSerializedTestRecord(record) if not isinstance(record, SpintopSerializedTestRecord) else record 
            for record in records
        ]

    @classmethod
    def from_features(cls, features):
        return cls(records=serialized_features_to_record_list(features))

    def deserialize(self, serializer):
        return (record.deserialize(serializer) for record in self.records)

def serialized_features_to_record_list(features):
    raise NotImplementedError('Not possible anymore.')
    test_uuid_record_map = OrderedDict()
    
    for feature in features:
        found_summary = None
        found_feature = None

        if is_serialized_type_of(feature, TestRecordSummary):
            found_summary = feature
        else:
            found_feature = feature
        
        test_uuid = TestUUID.get_value(feature)

        record = test_uuid_record_map.get(test_uuid, None)
        if record is None:
            record = SpintopSerializedTestRecord()
        
        if found_summary:
            if record.summary is not None:
                raise ValueError('Two features match as a top level record for the same record: {!r} and {!r}'.format(record.test_record, found_summary))
            record.summary = found_summary
        else:
            record.features.append(found_feature)

        test_uuid_record_map[test_uuid] = record
    
    records = list(test_uuid_record_map.values())

    for record in records:
        if record.summary is None:
            # Find a valid test_id from features.
            if SUPPORT_MISSING_TOP_LEVEL_RECORD:
                test_id = None
                if record.features:
                    test_id = record.features[0]['test_id']
                else:
                    raise ValueError('Empty Test Record.')
                record.summary = TestRecordSummary.null(test_id=test_id, original=False).as_dict()
            else:
                raise RuntimeError('Missing top level record from SpintopTestRecord {!r}'.format(record))

    return records

        
        
    