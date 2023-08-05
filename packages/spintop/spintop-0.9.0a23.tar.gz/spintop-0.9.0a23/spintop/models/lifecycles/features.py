from typing import Optional

from spintop.models import (
    MeasureFeatureRecord,
    PhaseFeatureRecord,
)


class LCFeature(MeasureFeatureRecord, PhaseFeatureRecord):
    uuid: str 
    record_uuid: str
    pipeline_uuid: str = None
    # name: str

    # version: int = 0
    # index: int = 0
    # depth: int = 0
    # outcome: OutcomeData = None

    # value_f: Optional[float]
    # value_s: Optional[str]

    # user_data: dict = dict
    # feature_count: int = 0 # Number of children

    # def __post_init__(self):
    #     super().__post_init__()
    #     if self.outcome:
    #         self.outcome = OutcomeData.create(self.outcome)