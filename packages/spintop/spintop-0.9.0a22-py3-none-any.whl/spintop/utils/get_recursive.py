from collections.abc import Mapping

class GetRecursiveMixin(object):
    
    def get_recursive(self, as_str=None, as_array=None):
        if as_str:
            as_array = as_str.split('.')
        
        this_attr_name, *as_array = as_array
        this_attr = self._get_attr_recursive(this_attr_name)
        

        if as_array:
            if not isinstance(this_attr, GetRecursiveMixin):
                this_attr = AnonymousGetRecursive(this_attr)
            return this_attr.get_recursive(as_array=as_array)
        else:
            return this_attr
    
    def _get_attr_recursive(self, name):
        return getattr(self, name)

class GetRecursiveKeyMixin(GetRecursiveMixin):

    def _get_attr_recursive(self, name):
        return self[name]

class AnonymousGetRecursive(Mapping, GetRecursiveMixin):
    def __init__(self, obj):
        self.obj = obj

    def _get_attr_recursive(self, name):
        if isinstance(self.obj, Mapping):
            return self.obj[name]
        else:
            try:
                return getattr(self.obj, name)
            except AttributeError:
                return self.obj[name]

    def __iter__(self):
        return self.obj.__iter__()

    def __len__(self):
        return self.obj.__len__()

    def __getattr__(self, name):
        return self._get_attr_recursive(name)

    def __getitem__(self, key):
        return self._get_attr_recursive(key)

class GetRecursiveAccessor():
    def __init__(self, name):
        self.name = name
    
    def __call__(self, obj):
        return AnonymousGetRecursive(obj).get_recursive(self.name)

GetRecursive = AnonymousGetRecursive
