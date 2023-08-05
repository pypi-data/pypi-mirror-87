from json import dumps, loads

from marshmallow import fields

from google.cloud.bigquery import SchemaField

from spintop.models import AbstractSchema, register_schema_type
from spintop.models.serialization import DeepTabularCompatSchema

def bigquery_schema_from_model(model_cls):
    jsonschema = model_cls.dump_json_schema()
    return build_schema(jsonschema)
    
BigQuerySchema = DeepTabularCompatSchema
register_schema_type('bigquery', DeepTabularCompatSchema)

def define_schema(field, name):
    schema_name = name
    schema_type = "STRING"
    schema_mode = "NULLABLE"
    schema_description = None
    schema_fields = ()

    if 'type' not in field and 'anyOf' in field:
        for types in field['anyOf']:
            if types['type'] == 'null':
                schema_mode = 'NULLABLE'
            else:
                field = types
            
    if isinstance(field['type'], list):
        types = set(field['type'])
        if "null" in types:
            schema_mode = 'NULLABLE'
            types.remove("null")
        else:
            schema_mode = 'required'
        
        if len(types) != 1:
            raise ValueError('BigQuery only supports one type per property, with the exception of null.')

        schema_type = list(types)[0]
    else:
        schema_type = field['type']
    if schema_type == "object":
        schema_type, schema_fields = build_object_field(field)
    if schema_type == "array":
        schema_type = field.get('items').get('type')
        schema_mode = "REPEATED"
        if schema_type == "object":
          schema_type, schema_fields = build_object_field(field.get('items'))


    if schema_type == "string":
        if "format" in field:
            if field['format'] == "date-time":
                schema_type = "timestamp"

    if schema_type == 'number':
        schema_type = 'FLOAT'

    return (schema_name, schema_type, schema_mode, schema_description, schema_fields)

def build_object_field(field):
    if 'properties' in field:
        return ("RECORD", build_schema(field))
    else:
        # expect JSON
        return ("STRING", ())

def build_schema(schema):
    SCHEMA = []
    for key in schema['properties'].keys():
        
        if not (bool(schema['properties'][key])):
            # if we endup with an empty record.
            continue

        schema_name, schema_type, schema_mode, schema_description, schema_fields = define_schema(schema['properties'][key], key)
        SCHEMA.append(SchemaField(schema_name, schema_type, schema_mode, schema_description, schema_fields))

    return SCHEMA