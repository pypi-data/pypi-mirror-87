
from ..base import BaseDataClass
from ..persistence import PersistenceIDRecord, PersistenceRecord, uuid_generator
from ..test_records import DutIDRecord

class UnitIDRecord(PersistenceIDRecord):
    dut: DutIDRecord
    
    def __post_init__(self):
        super().__post_init__()
        # possibly transform a string into dut id + version
        self.dut = DutIDRecord.create(self.dut)

        if self.uuid is None:
            self.uuid = uuid_generator(self.start_datetime, self.dut)

class UnitDataRecord(BaseDataClass):
    pass

class SpintopUnitRecord(PersistenceRecord):
    index: UnitIDRecord = UnitIDRecord
    data: UnitDataRecord = None