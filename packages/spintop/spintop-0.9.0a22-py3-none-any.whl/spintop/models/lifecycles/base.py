from spintop.models import VersionIDRecord, FeatureRecord
from spintop.models.persistence import ProcessStepIDRecord

from spintop.models import get_json_serializer

from .features import MeasureFeatureRecord, PhaseFeatureRecord, LCFeature
from .files import SpintopFileReference
from .steps import LCStep, LCUnit, LCTypes 

feature_fields = FeatureRecord.fields()
index_field = feature_fields.index

def record_to_lifecycle_step(record, pipeline_uuid=None, filename=None):

    step = cast_to(record, LCStep, units=[])

    add_unit_if_exists(step, record.dut, LCTypes.DUT)
    add_unit_if_exists(step, record.step, LCTypes.STEP)
    add_unit_if_exists(step, record.station, LCTypes.STATION)
    add_unit_if_exists(step, VersionIDRecord.create(record.operator), LCTypes.OPERATOR)
    step.pipeline_uuid = pipeline_uuid
    step.filename = filename
    return step

def add_unit_if_exists(step, version_id, lc_type):
    if version_id:
        step.units.append(LCUnit.from_version_id(version_id, lc_type))

def cast_to(record, cls, **others):
    cls_fields = set(field.field_name_ for field in cls.fields())

    data = {
        field.field_name_: field(record) for field in record.fields() if field.field_name_ in cls_fields
    }
    data.update(others)

    return cls(
        **data
    )

def feature_to_lifecycle_feature(record_uuid, feature, pipeline_uuid=None):
    feature_uuid = f'{record_uuid}-feat{index_field(feature)}'

    return cast_to(feature, LCFeature,  uuid=feature_uuid, record_uuid=record_uuid, pipeline_uuid=pipeline_uuid)


STREAM_SUFFIX = '_stream'

class LifecycleStream(object):
    def __init__(self, table_name, model_type, analytics, org_data):
        self.name = table_name
        self.stream_name = table_name + STREAM_SUFFIX
        self.model_type = model_type

        self.analytics = analytics
        self.org_data = org_data

        self.reserve()

    def update(self, raw_data):
        return self.analytics.update_named_stream(self.name, raw_data, stream_type=self.model_type)

    def singer_factory(self):
        return self.analytics.singer_factory(self.stream_name, record_cls=self.model_type)

    def on_stream_update(self, dataset_fns):
        pass
        # query = dataset_fns.map_stream_to_latest_views(self.stream_name)
        # # Virtual view
        # query.update_view(self.name)

    def reserve(self):
        self.analytics.reserve_stream_name(self.name, self.on_stream_update, stream_type=self.model_type, stream_name=self.stream_name)

class StepsLifecycle(LifecycleStream):

    def on_stream_update(self, dataset_fns):
        super().on_stream_update(dataset_fns)
        # Create dut states view table
        # org_config = self.org_data

        # table_name = self.name + '_dut'
        # config = org_config.get(table_name, {})

        # query = dataset_fns.lc_unit_yields(self.name, LCTypes.DUT, **config)
        # # Virtual view
        # query.update_view(table_name)

class FeaturesLifecycle(LifecycleStream):
    
    def on_stream_update(self, dataset_fns):
        super().on_stream_update(dataset_fns)
        # Create dut states view table
        org_config = self.org_data

        config = org_config.get('measures_marts', {})

        table_name = self.name + '_mart'

        for table_suffix, measures in config.items():
            mart_table_name = table_name + table_suffix
            query = dataset_fns.measure_values_mart(self.name, measure_names=measures)
            # Virtual view
            query.update_view(mart_table_name)

def reserve_lifecycle_streams(analytics, env):
    analytics.steps = StepsLifecycle('steps', LCStep, analytics, env['SPINTOP_DA_LC_STEPS'])
    analytics.features = FeaturesLifecycle('features', LCFeature, analytics, env['SPINTOP_DA_LC_FEATURES'])
    analytics.processed_files = LifecycleStream('files', SpintopFileReference, analytics, None)
