from textwrap import indent, dedent
import inspect
from reprlib import recursive_repr
from datetime import datetime
from collections.abc import Mapping

from dataclasses import dataclass, fields, _MISSING_TYPE, MISSING, field as dataclass_field, asdict

from spintop.utils import GetRecursiveMixin, GetRecursive, classproperty

from .view import DataClassPrimitiveView, ComplexPrimitiveView, join_key_prefix
from .meta import FieldsOf, MetaField
from .serialization import DataClassSchema, register_type, cls_of_obj, ValidationError, get_base_schema_cls, dump_json_schema

class CacheByCls():
    def __init__(self):
        self.value_by_cls = {}
        
    def retrieve(self, cls):
        if not self.value_by_cls.get(cls, None):
            self.value_by_cls[cls] = self._get(cls)
        return self.value_by_cls[cls]
    
    def _get(self, cls):
        raise NotImplementedError()
    
class FieldsCache(CacheByCls):
    """The fields() function is quite slow. This allows to store its 
    return value per cls, as it shouldn't change dynamically during
    runtime."""
    
    def _get(self, cls):
        return fields(cls)
    
class DefaultViewsCache(CacheByCls):
    def _get(self, cls):
        return DataClassPrimitiveView(
            cls.get_default_view_mapping()
        )

_fields_cache = FieldsCache()
_default_views_cache = DefaultViewsCache()

BaseDataClass = None # temporary define

def field_metadata(readonly=False, validate=None):
    return {
        'dump_only': readonly, # Marshmallow field key
        'validate': validate
    }

def is_field_readonly(field):
    return is_metadata_readonly(field.metadata)

def is_metadata_readonly(metadata):
    return metadata.get('dump_only', False)

def validate_field_value(field, value):
    validate = field.metadata.get('validate', None)
    if validate:
        validate(value)

def _model_dataclass(_register_type=None, schema_cls=None, **kwargs):
    """Custom dataclass decorator that removes the default values set on classes.
    This allows the meta base data class to return the field itself instead of the
    default value."""
    def _decorator(cls):
        
        # if not _base_cls and not issubclass(cls, BaseDataClass):
        #     cls = type(cls.__name__, (cls, BaseDataClass), {'__annotations__': get_annotations(cls)})

        model_properties = {}
        # Extract all properties from the data class and replace them by their
        # respective fields. 
        annotations = get_annotations(cls)

        for attr_name in dir(cls):
            if isinstance(getattr(cls, attr_name), _AbstractModelAttribute):
                return_type = annotations.get(attr_name, None)
                # If it has no return type, then it probably is not the fget accessor.
                if return_type:
                    prop = getattr(cls, attr_name)
                    model_properties[attr_name] = prop

                    prop.set_return_type(return_type)
                    setattr(cls, attr_name, prop.field)

        cls = dataclass(init=False, repr=False, **kwargs)(cls)

        # Once the dataclass is done and it detected the different fields,
        # replace the attributes by the final property accessor.
        for attr_name, prop in model_properties.items():
            value = prop.value_to_set_on_cls()
            if value is not None:
                setattr(cls, attr_name, value)

        register_type(cls, _register_type, schema_cls=schema_cls)
        return cls
    return _decorator

def get_annotations(obj):
    return obj.__dict__.get('__annotations__', {})

def set_annotations(obj, anno):
    obj.__dict__['__annotations__'] = anno

class _AbstractModelAttribute():
    def __init__(self, readonly=False, validators=[], **kwargs):
        self.readonly = readonly
        self.validators = validators
        self.field_kwargs = kwargs
        self._field = None
    
    @property
    def field(self):
        if self._field is None:
            kwargs = self.field_kwargs
            kwargs['metadata'] = self._metadata()
            self._field = dataclass_field(**kwargs)
        return self._field

    def set_return_type(self, return_type):
        pass

    def value_to_set_on_cls(self):
        return None

    def validate(self, value):
        for validator in self.validators:
            validator(value)
    
    def _metadata(self):
        return field_metadata(readonly=self.readonly, validate=self.validate)

class model_attribute(_AbstractModelAttribute):
    def __init__(self, default_factory, validators=[], **kwargs):
        super().__init__(default=default_factory, validators=validators, **kwargs)

class model_property(_AbstractModelAttribute):
    def __init__(self, fget=None, fset=None, fdel=None, doc=None, readonly=True, **kwargs):
        super().__init__(readonly=readonly, **kwargs)
        self.property = property(fget, fset, fdel, doc)

    def value_to_set_on_cls(self):
        return self.property

    def set_return_type(self, return_type):
        annotations = get_annotations(self.property.fget)
        annotations['return'] = return_type
        set_annotations(self.property.fget, annotations)

    def getter(self, fget):
        self.property = self.property.getter(fget)
        return self

    def setter(self, fset):
        self.property = self.property.setter(fset)
        return self

    def deleter(self, fdel):
        self.property = self.property.deleter(fdel)
        return self

def model_constant(value):
    return model_property(
        fget= lambda obj: value,
        readonly=True
    )

class MetaBaseDataClass(type):
    """Allows to replace a dataclass decorator with inheritance."""

    def __new__(cls, name, mro, attrs):
        _type = attrs.get('register_type_', attrs.get('__qualname__', name))
        # _base_cls = attrs.get('_base_cls', False)
        _schema_cls = attrs.get('schema_cls_', None)

        cls = super(MetaBaseDataClass, cls).__new__(cls, name, mro, attrs)

        # create dataclass
        dataclass = _model_dataclass(_type, schema_cls=_schema_cls)(cls)

        fields_docs = ""
        for field in dataclass.fields():
            field_docs = dedent(field.__doc__)

            field_key_and_docs = indent(f"\n**{field.field_name_}**:{field_docs}", 8*' ')
            fields_docs += field_key_and_docs

        # format class docs with the 'fields_docs' attribute with 
        dataclass.__doc__ = dedent(dataclass.__doc__.format(fields_docs=fields_docs))
        
        return dataclass

class BaseDataClass(GetRecursiveMixin, metaclass=MetaBaseDataClass):
    register_type_ = '_base'
    schema_cls_ = None
    fields_docs_ = {}

    def __init__(self, *args, **kwargs):
        if args:
            raise NotImplementedError('Positionnal args not supported with BaseDataClass descendants.')
        defaults = self.get_defaults()

        self.update_attrs(defaults) # First set defaults
        self.update_attrs(kwargs) # Then constructor arguments.
        self.__post_init__()

        # Check if fields exist (or property)
        self.validate_attrs(kwargs)

    def __post_init__(self):
        pass

    @classmethod
    def field_doc(cls, field_name):
        return cls.fields_docs_.get(field_name, 'No documentation.')

    @classmethod
    def defaults(cls, **others):
        return others

    @classmethod
    def get_defaults(cls, **other_fields):
        defaults = cls.defaults()
        defaults.update({
            field.name: 
                default_field_value(field) for field in cls.dataclass_fields() if field.name not in defaults and not is_field_readonly(field)
        })
        return defaults
    
    @classmethod
    def null(cls, **not_null_fields):
        """ Creates an instance with all attributes set to None. 
        Calls null() on any sub- BaseDataClass fields.
        """
        arguments = {}

        for key, default in cls.get_defaults().items():    
            arguments[key] = default
        
        arguments.update(not_null_fields)
        return cls(**arguments)
    
    @classmethod
    def dataclass_fields(cls):
        return _fields_cache.retrieve(cls)
    
    @classmethod
    def get_property_attrs(cls, with_setter_only=False):
        properties = set()
        for attr in dir(cls):
            value = getattr(cls, attr)
            if isinstance(value, property):
                if not with_setter_only or value.fset:
                    properties.add(attr)
        return properties

    @classmethod
    def data_dataclass_fields(cls):
        """ Sub classed by FeatureRecord below.
        """
        return cls.dataclass_fields()
        
    @classmethod
    def fields(cls):
        """Returns a FieldsOf object that allows to access the MetaFields of this cls.
        This allows a type based access to the underlying fields for query building.
        
        Examples:
            - Get the MetaField itself:
                >>> PersistenceRecord.fields().index.uuid
                MetaField(PersistenceRecord.index.uuid)

            - Get the complete dot separated name of this field:
                >>> PersistenceRecord.fields().index.uuid.name_
                'index.uuid'

            - Get the value of the MetaField of an instance of this type:
                >>> record = PersistenceRecord(index=PersistenceIDRecord(uuid='x'))
                >>> uuid_field = PersistenceRecord.fields().index.uuid
                >>> uuid_field.get_value(record)
                'x'
        """
        return FieldsOf(cls)

    @classmethod
    def get_default_view(cls):
        return _default_views_cache.retrieve(cls)
        
    @classmethod
    def get_default_view_mapping(cls, with_key_prefix=None):
        if with_key_prefix is not None:
            key_creator = lambda key: join_key_prefix(with_key_prefix, key)
        else:
            key_creator = lambda key: key
        
        # The default view uses the fields defined by the data_dataclass_fields class method.
        fields = cls.data_dataclass_fields()
        
        return {key_creator(field.name): MetaField(cls, field) for field in fields}

    @classmethod
    def get_schema(cls, schema_key=None, schema_type=None):
        if schema_type is None:
            schema_type = get_base_schema_cls(schema_key)
        return DataClassSchema(cls, schema_type)

    @classmethod
    def dump_json_schema(cls):
        return dump_json_schema(cls)

    @classmethod
    def from_dict(cls, data, schema_type=None):
        return cls.get_schema(schema_type)().load(data)

    def as_dict(self, schema_type=None):
        return self.get_schema(schema_type)().dump(self)

    def validate_attrs(self, other_attrs):
        # dataclass_fields = {field.name: field for field in self.dataclass_fields()}
        fields = {field.field_name_: field for field in self.fields()}

        unsupported_keys = set()

        other_attrs.update({key: getattr(self, key) for key in fields})

        for key, value in other_attrs.items():
            meta_field = fields.get(key)
            if not meta_field:
                possible_property = getattr(self.__class__, key, None)
                if isinstance(possible_property, property):
                    pass # OK.
                else:
                    # does not exist
                    unsupported_keys.add(key)
            else:
                field_obj = meta_field.field_
                if value is not None and isinstance(field_obj.type, type) and not isinstance(value, field_obj.type):
                    raise ValidationError(f'{self.__class__.__name__} attribute {key} has wrong type {type(value)}; requires {field_obj.type}')
                try:
                    validate_field_value(field_obj, value)
                except ValidationError as e:
                    raise ValidationError(f'{self.__class__.__name__} attribute {key} failed validation: {str(e)}')

        if unsupported_keys:
            settable_properties = self.get_property_attrs(with_setter_only=True)
            raise TypeError(f'{self.__class__.__name__} got unexpected argument(s) {unsupported_keys!r}. Fields are: {fields.keys()!r} and the following settable properties: {settable_properties!r}')

    def update_attrs(self, attributes_dict):
        for key, value in attributes_dict.items():
            setattr(self, key, value)
    
    def copy(self, with_data=True, as_cls=None, set_attributes={}):
        if with_data:
            nullify_fields = []
        else:
            nullify_fields = self.data_dataclass_fields()
            
        copy_obj = copy_nullify_fields(self, nullify_fields, target_cls=as_cls)
        for name, value in set_attributes.items():
            setattr(copy_obj, name, value)
        return copy_obj
    

    def getattr_from_field(self, meta_field):
        return getattr_from_field(self, meta_field)

    def hasattr_from_field(self, meta_field):
        return hasattr_from_field(self, meta_field)

    @recursive_repr()
    def __repr__(self):
        fields = tuple("{}={}".format(field.name, repr(getattr(self, field.name, None))) for field in self.dataclass_fields())
        return "{}({})".format(self.__class__.__name__, ", ".join(fields))


def getattr_from_field(obj, meta_field):
    return meta_field.get_value(obj)

def hasattr_from_field(obj, meta_field):
    try:
        getattr_from_field(obj, meta_field)
        return True
    except AttributeError:
        return False


def copy_nullify_fields(obj, null_fields, target_cls=None):
    if target_cls is None:
        target_cls = obj.__class__
    
    copy_obj = target_cls.null()
    not_null_fields = (set(obj.dataclass_fields()) - set(null_fields)) & set(target_cls.dataclass_fields())
    for field in not_null_fields:
        setattr(copy_obj, field.name, getattr(obj, field.name))
    
    return copy_obj

def default_field_value(field):
    if not isinstance(field.default_factory, _MISSING_TYPE):
        value = field.default_factory()
    elif not isinstance(field.default, _MISSING_TYPE):
        if callable(field.default):
            value = field.default()
        else:
            value = field.default
    else:
        value = None
    
    return value

def default_cls_missing_view_fn(data_obj):
    cls = cls_of_obj(data_obj)
    return cls.get_default_view()

class DefaultPrimitiveView(ComplexPrimitiveView):
    def __init__(self, cls_missing_view_fn=None):
        if cls_missing_view_fn is None:
            cls_missing_view_fn = default_cls_missing_view_fn

        super(DefaultPrimitiveView, self).__init__(
            BaseDataClass, 
            cls_missing_view_fn=cls_missing_view_fn
        )