from collections.abc import Mapping
from marshmallow import Schema, ValidationError


class OneOfSchema(Schema):
    """
    This is a special kind of schema that actually multiplexes other schemas
    based on object type. When serializing values, it uses get_obj_type() method
    to get object type name. Then it uses `type_schemas` name-to-Schema mapping
    to get schema for that particular object type, serializes object using that
    schema and adds an extra "type" field with name of object type.
    Deserialization is reverse.
    Example:
        class Foo(object):
            def __init__(self, foo):
                self.foo = foo
        class Bar(object):
            def __init__(self, bar):
                self.bar = bar
        class FooSchema(marshmallow.Schema):
            foo = marshmallow.fields.String(required=True)
            @marshmallow.post_load
            def make_foo(self, data, **kwargs):
                return Foo(**data)
        class BarSchema(marshmallow.Schema):
            bar = marshmallow.fields.Integer(required=True)
            @marshmallow.post_load
            def make_bar(self, data, **kwargs):
                return Bar(**data)
        class MyUberSchema(marshmallow.OneOfSchema):
            type_schemas = {
                'foo': FooSchema,
                'bar': BarSchema,
            }
            def get_obj_type(self, obj):
                if isinstance(obj, Foo):
                    return 'foo'
                elif isinstance(obj, Bar):
                    return 'bar'
                else:
                    raise Exception('Unknown object type: %s' % repr(obj))
        MyUberSchema().dump([Foo(foo='hello'), Bar(bar=123)], many=True)
        # => [{'type': 'foo', 'foo': 'hello'}, {'type': 'bar', 'bar': 123}]
    You can control type field name added to serialized object representation by
    setting `type_field` class property.
    """

    type_field = "type"
    type_field_remove = True
    type_schemas = []

    def get_obj_type(self, obj):
        """Returns name of object schema"""
        return obj.__class__.__name__

    @property
    def strict_casting(self):
        return getattr(self, "context", {}).get('strict_casting', False)

    def has_own_fields(self):
        return bool(set(self.declared_fields) - {self.type_field})

    def dump(self, obj, *, many=None, **kwargs):
        errors = {}
        result_data = []
        result_errors = {}
        many = self.many if many is None else bool(many)
        if not many:
            try:
                result = result_data = self._dump(obj, **kwargs)
            except ValidationError as error:
                result_errors = error.normalized_messages()
                result_data.append(error.valid_data)
        else:
            for idx, o in enumerate(obj):
                try:
                    result = self._dump(o, **kwargs)
                    result_data.append(result)
                except ValidationError as error:
                    result_errors[idx] = error.normalized_messages()
                    result_data.append(error.valid_data)

        result = result_data
        errors = result_errors

        if not errors:
            return result
        else:
            exc = ValidationError(errors, data=obj, valid_data=result)
            raise exc

    def _dump(self, obj, *, update_fields=True, **kwargs):

        context = getattr(self, "context", {})

        # Returns None only if the field is present, but the class is not registered.
        obj_type = self.get_obj_type(obj)

        obj_type = context.pop(self.type_field, obj_type)
        
        if self.strict_casting and self.has_own_fields():
            # Dump as is.
            result = super(OneOfSchema, schema).dump(obj, many=False, **kwargs)
        else:
            
            if isinstance(obj, Mapping):
                # return mapping as-is, the obj_type is defined, but possibly not understood.
                return obj
            
            if not obj_type:
                raise ValidationError(
                    {"_schema": "Unknown object class: %s" % obj.__class__.__name__},
                )

            type_schema = self.type_schemas.get(obj_type)

            if not type_schema:
                raise ValidationError({"_schema": "Unsupported object type: %s" % obj_type})

            schema = type_schema if isinstance(type_schema, Schema) else type_schema()

            schema.context.update(context)

            if isinstance(schema, OneOfSchema):
                if isinstance(obj, Mapping):
                    # Already dumped and as an obj_type.
                    result = obj
                else:
                    result = super(OneOfSchema, schema).dump(obj, many=False, **kwargs)
            else:
                result = schema.dump(obj, many=False, **kwargs)

        if result is not None:
            result[self.type_field] = obj_type
        return result

    def load(self, data, *, many=None, partial=None, unknown=None):
        errors = {}
        result_data = []
        result_errors = {}
        many = self.many if many is None else bool(many)
        if partial is None:
            partial = self.partial
        if not many:
            try:
                result = result_data = self._load(
                    data, partial=partial, unknown=unknown
                )
                #  result_data.append(result)
            except ValidationError as error:
                result_errors = error.normalized_messages()
                result_data.append(error.valid_data)
        else:
            for idx, item in enumerate(data):
                try:
                    result = self._load(item, partial=partial)
                    result_data.append(result)
                except ValidationError as error:
                    result_errors[idx] = error.normalized_messages()
                    result_data.append(error.valid_data)

        result = result_data
        errors = result_errors

        if not errors:
            return result
        else:
            exc = ValidationError(errors, data=data, valid_data=result)
            raise exc

    def _load(self, data, *, partial=None, unknown=None):
        if not isinstance(data, dict):
            raise ValidationError({"_schema": "Invalid data type: %s" % data})

        data = dict(data)
        unknown = unknown or self.unknown

        context = getattr(self, "context", {})

        data_type = data.get(self.type_field)

        if self.strict_casting:
            data_type = context.pop(self.type_field, data_type)

        elif not data_type and self.type_field in context:
            data_type = context[self.type_field]

        if data_type:
            data[self.type_field] = data_type

        if not data_type:
            if self.has_own_fields():
                # This schema contains fields, load it.
                return super().load(data, many=False, partial=partial, unknown=unknown)
            else:
                raise ValidationError(
                    {self.type_field: ["Missing data for required field."]}
                )

        try:
            type_schema = self.type_schemas.get(data_type)
        except TypeError:
            # data_type could be unhashable
            raise ValidationError({self.type_field: ["Invalid value: %s" % data_type]})

        if not type_schema:
            raise ValidationError(
                {self.type_field: ["Unsupported value: %s" % data_type]}
            )

        schema = type_schema if isinstance(type_schema, Schema) else type_schema()

        schema.context.update({'strict_casting': self.strict_casting})

        if schema is self or self.__class__ is type_schema:
            return self._super_load(data, partial, unknown)
        else:
            return schema.load(data, many=False, partial=partial, unknown=unknown)

    def _super_load(self, data, partial, unknown):
        if self.type_field in data and self.type_field_remove:
            data.pop(self.type_field)
        return super().load(data, many=False, partial=partial, unknown=unknown)

    def validate(self, data, *, many=None, partial=None):
        try:
            self.load(data, many=many, partial=partial)
        except ValidationError as ve:
            return ve.messages
        return {}