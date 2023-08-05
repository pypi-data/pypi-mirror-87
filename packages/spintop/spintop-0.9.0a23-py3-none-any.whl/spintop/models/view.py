from collections.abc import Mapping
from collections import OrderedDict

from .meta import MetaField

from spintop.utils.dict_ops import (
    update, 
    deepen_value_in_dict,
    deepen_dict,
    flatten_dict,
    DEFAULT_PLACEHOLDER
)
from spintop.utils.get_recursive import GetRecursive

class _MetaFieldAccessor(object):
    def __init__(self, meta_field):
        self.field = meta_field

    def __call__(self, obj):
        return self.field.get_value(obj)

    def __repr__(self):
        return repr(self.field)

class _ValueAccessor(object):
    def __init__(self, value):
        self.value = value
    
    def __call__(self, obj):
        return self.value

    def __repr__(self):
        return f'Value({repr(self.value)})'
    
class _CallableAccessor(object):
    def __init__(self, fn):
        self.fn = fn

    def __call__(self, obj):
        return self.fn(GetRecursive(obj))

    def __repr__(self):
        return f'Call({self.fn.__name__}: {self.fn!r})'
    
class DataClassPrimitiveView(object):
    def __init__(self, key_values_mapping={}):
        self.build_accessors(key_values_mapping)
        
    def build_accessors(self, key_values_mapping):
        """ Creates a dict of callable
        """

        self._accessors_mapping = _build_accessors(key_values_mapping)
        
    def apply(self, data_obj, flatten_dict=False, key_prefix=None, attribute_error_policy='ignore'):
        result = {}
        prefix_accessor = None

        if key_prefix:
            prefix_accessor = _build_single_accessor(key_prefix)

        raise_attribute_errors = attribute_error_policy != 'ignore'
        for accessor_key, accessor_value in self._accessors_mapping.items():
            # Set to none if does not exist.
            key = None

            if prefix_accessor:
                complete_key = prefix_accessor + accessor_key
            else:
                complete_key = accessor_key

            try:
                key = _apply_single_accessor(complete_key, data_obj)
                value = _apply_single_accessor(accessor_value, data_obj)
            except (AttributeError, KeyError) as e:
                if raise_attribute_errors:
                    raise
                else:
                    _apply_key_value(result, key, DEFAULT_PLACEHOLDER, flatten_dict)
                    continue
            
            _apply_key_value(result, key, value, flatten_dict)
        
        return result

def _build_accessors(key_values_mapping):
    flat_key_values_mapping = flatten_dict(key_values_mapping)
    return {_build_single_accessor(key): _build_single_accessor(value) for key, value in flat_key_values_mapping.items()}

def _build_single_accessor(obj):
    if isinstance(obj, tuple):
        return tuple(_build_single_accessor(subobj) for subobj in obj)
    elif isinstance(obj, MetaField) or isinstance(obj, property):
        return _MetaFieldAccessor(obj)
    # elif isinstance(obj, property):
    #     return _PythonAccessor(obj)
    elif callable(obj):
        return _CallableAccessor(obj) # Obj is an accessor
    else:
        return _ValueAccessor(obj) # Will always return obj
    
def _apply_single_accessor(accessor, obj):
    if isinstance(accessor, tuple):
        return tuple(_apply_single_accessor(subaccessor, obj) for subaccessor in accessor)
    else:
        return accessor(obj)

def default_cls_missing_view_fn(data_obj):
    raise NotImplementedError()

def _apply_key_value(_dict, key, value, flatten_dict):
    if isinstance(value, Mapping):
        # Push keys from a value dictionnary into the key itself.
        # the rest of the code will handle flatten_dict well enough
        # I.e. if key = (key,) & value = {'foo': 'bar', 'bar':'foo'}, this will call
        # this function with 
        #   key=(key, foo), value=bar AND 
        #   key=(key, bar), value=foo
        for subkey, subvalue in value.items():
            _apply_key_value(_dict, key + (subkey,), subvalue, flatten_dict)

    elif isinstance(key, tuple) and not flatten_dict:
        # Push value deep into a nested dictionnary
        # key = (x, y, z)
        # result.update({x: {y: {z: value}}})
        update(_dict, deepen_value_in_dict(key, value))
    else:
        # or keep as is (flat)
        # key = (x, y, z)
        # result[(x, y, z)] = value
        _dict[key] = value

class ComplexPrimitiveView(object):
    def __init__(self, base_cls, cls_missing_view_fn=None):
        if cls_missing_view_fn is None: cls_missing_view_fn = default_cls_missing_view_fn
        
        self.base_cls = base_cls
        self.cls_missing_view_fn = cls_missing_view_fn
        self.custom_views = {}
        
    def _find_closest_parent(self, cls):
        closest_parent = None
        
        if cls in self.custom_views:
            return cls
        
        for match_cls in self.custom_views:
            possible_parent = None
            if issubclass(cls, match_cls):
                possible_parent = match_cls
            
            if possible_parent and (closest_parent is None or issubclass(possible_parent, closest_parent)):
                # possible parent is closer to cls than the previous closest parent.
                closest_parent = possible_parent
                
        return closest_parent
    
    def _find_view(self, data_obj):
        cls = data_obj.__class__
        best_match = self._find_closest_parent(cls)
        if best_match:
            return self.custom_views[best_match]
        else:
            return self.cls_missing_view_fn(data_obj)
    
    def add_view(self, cls, view_mapping):
        self.custom_views[cls] = DataClassPrimitiveView(view_mapping)
        
    def apply(self, root_data_obj, flatten_dict=False, key_prefix=None, **apply_kwargs):
        flatten_key_prefix = None
        if flatten_dict:
            if key_prefix is None:
                flatten_key_prefix = ()
            else:
                flatten_key_prefix = key_prefix
        
        result = self._apply_data_obj(root_data_obj, flatten_key_prefix=flatten_key_prefix, **apply_kwargs)

        if not flatten_dict and key_prefix:
            return deepen_value_in_dict(key_prefix, result)
        else:
            return result
    
    def _apply_data_obj(self, data_obj, flatten_key_prefix=None, **apply_kwargs):
        mapping = self._find_view(data_obj).apply(data_obj, flatten_dict=flatten_key_prefix is not None, **apply_kwargs)
        
        flatten_key_prefix_built = _build_single_accessor(flatten_key_prefix)
        flatten_key_prefix_applied = _apply_single_accessor(flatten_key_prefix_built, data_obj)

        return self._apply_mapping(mapping, flatten_key_prefix=flatten_key_prefix_applied, **apply_kwargs)
    
    def _apply_mapping(self, mapping, flatten_key_prefix=None, **apply_kwargs):
        result = OrderedDict()
        
        for key, value in mapping.items():
            
            flat_key = None
            if flatten_key_prefix is not None:
                flat_key = join_key_prefix(flatten_key_prefix, key)
            
            discard_false_subvalue = False 
            
            if isinstance(value, self.base_cls):
                subvalue = self._apply_data_obj(value, flatten_key_prefix=flat_key, **apply_kwargs)
                # If bool(subvalue) is False, then the sub-view returned an empty mapping or None. Do not consider it.
                discard_false_subvalue = True 
            elif isinstance(value, Mapping):
                subvalue = self._apply_mapping(value, flatten_key_prefix=flat_key, **apply_kwargs)
                # If bool(subvalue) is False, the mapping is empty or none. Do not consider it.
                discard_false_subvalue = True 
            elif flat_key is not None:
                # limit case.
                # If flatten, we will .update the result instead of applying
                subvalue = {flat_key: value}
            else:
                subvalue = value
            
            if discard_false_subvalue and not subvalue:
                continue # discard
            
            if flat_key:
                for subkey in subvalue:
                    if subkey in result:
                        print("{} already in result.".format(subkey))
                update(result, subvalue)
            else:
                if key in result:
                    print("{} already in result.".format(key))
                update(result, {key: subvalue})
        
        return result

def join_key_prefix(key_prefix, key):
    if not isinstance(key, tuple):
        key = (key,)

    if not isinstance(key_prefix, tuple):
        key_prefix = (key_prefix,)
        
    return key_prefix + key

