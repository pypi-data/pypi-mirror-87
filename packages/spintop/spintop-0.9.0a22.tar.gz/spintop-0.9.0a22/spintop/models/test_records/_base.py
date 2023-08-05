""" Storage-friendly internal data classes. """
import numbers

from collections import defaultdict
from collections.abc import Mapping
from base64 import urlsafe_b64decode, urlsafe_b64encode
from uuid import UUID, uuid4

from datetime import datetime
from dataclasses import dataclass, fields, _MISSING_TYPE, MISSING, field, asdict
from typing import Union, List, Optional, Dict

from ..serialization import cls_of_obj

from ..base import (
    BaseDataClass, 
    _fields_cache,
    model_property
)

from ..common import DutIDRecord, TestbenchIDRecord, OutcomeData

from ..persistence import QualityStepIDRecord, uuid_generator

from ..view import ComplexPrimitiveView

from spintop.utils import isnan, utcnow_aware

NAME_SEPARATOR = ':'

def compute_stats(features):
    name_tuple_to_count_map = defaultdict(int)

    for feature in features:
        # For feature ('x', 'y', 'z'), increment ('x',), ('x', 'y') and ('x', 'y', 'z')
        name_tuple = feature.name_tuple

        for i in range(1, len(name_tuple)):
            sub_name = name_tuple[:i]
            name_tuple_to_count_map[sub_name] += 1

    for feature in features:
        feature.feature_count = name_tuple_to_count_map[feature.name_tuple]


class FeatureRecordNoData(BaseDataClass):
    """ Feature ID is determined by its name.
    """
    oid: Optional[str]
    name: Optional[str] = ''
    description: str = ''
    version: int = 0
    depth: int = 0
    index: int = 0
    ancestors: List[str] = list
    original: bool = True
    
    @classmethod
    def defaults(cls, **others):
        others['name'] = others.get('name', '')
        others['ancestors'] = others.get('ancestors', [])
        return super().defaults(**others)

    @classmethod
    def data_dataclass_fields(cls):
        """ The data fields are all fields except the ones declare up to this cls
        in the cls MRO.
        
        If a subclass defines only a dataclass field 'foo', this method will return
        foo only as a data field.
        """
        return set(_fields_cache.retrieve(cls)) - set(_fields_cache.retrieve(FeatureRecordNoData))
    
    @property
    def name_tuple(self):
        return tuple(self.ancestors) + (self.name,)

    @property
    def complete_name(self) -> str:
        return NAME_SEPARATOR.join(self.name_tuple)
    
class FeatureRecord(FeatureRecordNoData):
    # user_data: Dict[str, Optional[Any]] = dict 
    user_data: dict = dict
    outcome: OutcomeData = OutcomeData
    feature_count: int = 0 # Number of children
    
    def __post_init__(self):
        super().__post_init__()
        self.outcome = OutcomeData.create(self.outcome)

    @property
    def total_feature_count(self):
        return self.feature_count

    @classmethod
    def defaults(cls, **others):
        others['user_data'] = others.get('user_data', {})
        others['feature_count'] = others.get('feature_count', 0)
        return super(FeatureRecord, cls).defaults(**others)
    
class PhaseFeatureRecord(FeatureRecord):
    duration: Optional[float] = None
    
class TestIDRecord(QualityStepIDRecord, PhaseFeatureRecord):
    testbench: TestbenchIDRecord = model_property()

    @testbench.getter
    def testbench(self):
        return self.step

    @testbench.setter
    def testbench(self, value):
        self.step = value

    @property
    def testbench_name(self) -> Optional[str]:
        return self.testbench.id

    @testbench_name.setter
    def testbench_name(self, value):
        self.testbench.id = value


TestRecordSummary = TestIDRecord # backward compat

class MeasureFeatureRecord(FeatureRecord):
    value_f: Optional[float]
    value_s: Optional[str]

    @property
    def value(self) -> Union[float, str, None]:
        if self.value_f is not None:
            return self.value_f
        else:
            return self.value_s

    @value.setter
    def value(self, value):
        if value is None or isinstance(value, str):
            self.value_f = None
            self.value_s = value
        elif isinstance(value, numbers.Number):
            self.value_f = value
            self.value_s = None
        else:
            raise ValueError('Only string or numeric types are supported. Received {!r} of type {}'.format(value, type(value)))
    
class DutOp(BaseDataClass):
    dut_match: DutIDRecord
    dut_after: DutIDRecord
    op_datetime: datetime = utcnow_aware
    
    @classmethod
    def create(cls, dut_match, dut_after, op_datetime):
        return cls(
            dut_match=DutIDRecord.create(dut_match),
            dut_after=DutIDRecord.create(dut_after),
            op_datetime=op_datetime
        )
    
    def does_applies_to(self, dut, on_datetime):
        return self.dut_match.match(dut) and self.op_datetime < on_datetime
    
    def apply_or_return(self, dut, on_datetime):
        if self.does_applies_to(dut, on_datetime):
            return self.apply(dut)
        else:
            return dut
        
    def apply(self, dut):
        """Apply op to dut. Does not check for datetime. """
        new_dut = self.dut_after.copy()
        if new_dut.id is None:
            new_dut.id = dut.id
        return new_dut
        