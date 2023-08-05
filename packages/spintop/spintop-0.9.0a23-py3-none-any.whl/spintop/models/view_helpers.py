from .meta import FieldsOf
from .test_records import MeasureFeatureRecord

def value_of_feature_named(name):
    measure_fields = FieldsOf(MeasureFeatureRecord)
    name_field = measure_fields.name.name_
    value_fields = [
        measure_fields.value_f.name_,
        measure_fields.value_s.name_,
    ]
    def _accessor(feat):
        if feat.get_recursive(name_field) != name:
            raise AttributeError('Wrong feature')
        else:
            for value_field in value_fields:
                value = feat.get_recursive(value_field)
                if value is not None:
                    break
            return value
    return _accessor