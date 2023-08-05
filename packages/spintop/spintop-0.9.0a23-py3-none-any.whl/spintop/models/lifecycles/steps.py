from typing import List
from enum import Enum
from datetime import datetime

from spintop.models import (
    BaseDataClass,
    PersistenceIDRecord,
    OutcomeData,
    VersionIDRecord
)

class LCTypes():
    DUT = 'dut'
    STATION = 'station'
    OPERATOR = 'operator'
    SOFTWARE = 'software'
    STEP = 'step'

class LCUnit(VersionIDRecord):
    lc_type: str = ''

    @classmethod
    def from_version_id(cls, version_id, lc_type):
        return cls(
            id=version_id.id,
            version=version_id.version,
            lc_type=lc_type
        )

class LCStep(PersistenceIDRecord):
    """
    Steps represent a distinct production event. 
    
    Each row is a particular event with a date and time, an outcome and multiple associated lifecycle units.

    ## Lifecycle Unit

    Each step references many lifecycle units. Only one of these units, 

    ## Lifecycle Type

    This is the unit type that will be tracked throughout the production line. 
    Say a certain step represents a system test at the step 'system test', executed
    by operator 'Mike'. The system ID is 'SYS01' and a board with ID 'BOARD01' is 
    assembled in this system. The step units should be:

    units:
    - LCUnit(lc_type='system', id='SYS01')
    - LCUnit(lc_type='board', id='BOARD01')
    - LCUnit(lc_type='step', id='system test')
    - LCUnit(lc_type='operator', id='Mike')
    
    And, because the DUT is the system, the lc_type attribute of the step itself
    should be 'system'.
    """
    
    fields_docs_ = dict(
        outcome=OutcomeData.__doc__,
        duration="""
    The duration in seconds of this step. Use None/null if unknown.
        """,
        lc_type="""
    This represents the lifecycle type of this main lifecycle unit of this step. 
    See the lifecycle type section of LCStep documentation.
        """,
        units="""
    The list of lifecycle units associated with this step. One of those is the 'main'
    device under test (DUT) as determined by the lc_type attribute.
        """

    )
    fields_docs_.update(PersistenceIDRecord.fields_docs_)

    outcome: OutcomeData = None
    duration: float = None
    lc_type: str = None # The lifecycle of this step. Linked with the units lc_types.
    units: List[LCUnit] = list
    filename: str = None
    pipeline_uuid: str = None
    
    def __post_init__(self):
        super().__post_init__()
        if self.outcome is not None:
            self.outcome = OutcomeData.create(self.outcome)
