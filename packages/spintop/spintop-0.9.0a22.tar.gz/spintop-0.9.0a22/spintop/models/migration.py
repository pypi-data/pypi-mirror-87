
def DeprecatedBy(new_cls):
    class _Temp():
        def __new__(cls, **data):
            data = cls.migrate(data)
            return new_cls(**data)
        
        @classmethod
        def migrate(cls, data):
            raise NotImplementedError()

    _Temp.__name__ = f'TransformTo{new_cls.__name__}'
    return _Temp