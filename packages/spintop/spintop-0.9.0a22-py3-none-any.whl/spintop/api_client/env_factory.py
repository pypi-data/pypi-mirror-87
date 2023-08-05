import re
from collections import namedtuple
from typing import List, Dict, Any, Optional
import datetime as dt


from spintop.models import BaseDataClass

from .models import OrgDataEnv, EnvDataspecs, DimensionSpec, TableSpec

def create_env_from_spintop_metadata(spintop_metadata):
    metadata_factories = {
        'dbt': create_env_from_dbt_metadata
    }

    meta_style = spintop_metadata.get('style', None)

    if not meta_style:
        raise ValueError('Metadata is missing "style" field.')

    factory = metadata_factories.get(meta_style, None)

    if not factory:
        raise ValueError(f'Metadata style {meta_style!r} is not supported.')

    return factory(spintop_metadata)

class Versions(BaseDataClass):
    spintop: str
    spintop_da: str

class SpintopDAVariables(BaseDataClass):
    step_nodes: dict
    transitions: dict

    def as_vars(self):
        all_vars = {}
        fields = list()
        for field in self.fields():
            all_vars['spintop_da:' + field.field_name_] = field.get_value(self)
        return all_vars

class BigQueryTableSchema(BaseDataClass):
    table_catalog: str
    table_schema: str
    table_name: str
    table_type: str
    is_insertable_into: str
    is_typed: str
    creation_time: str

class BigQueryColumnSchema(BaseDataClass):
    table_catalog: str
    table_schema: str
    table_name: str
    column_name: str
    ordinal_position: int = None
    is_nullable: str = None
    data_type: str
    is_generated: str = None
    generation_expression: str = None
    is_stored: str = None
    is_hidden: str = None
    is_updatable: str = None
    is_system_defined: str = None
    is_partitioning_column: str = None
    clustering_ordinal_position: int = None

class DBTStyleMetadata(BaseDataClass):
    dataset_id: str
    project_id: str
    target: Dict[str, Optional[Any]] = dict
    last_run_at: str
    dbt_graph: str ## It's json, but so complex that the parser cannot handle it. Keep as str.
    versions: Versions
    spintop_da_vars: SpintopDAVariables
    dataset_tables: List[BigQueryTableSchema]
    ref_columns: List[BigQueryColumnSchema]

def create_env_from_dbt_metadata(metadata):
    schema = DBTStyleMetadata.get_schema('tabular')()
    metadata = schema.load(metadata)

    columns = index_columns_by_table_name_dot_column_name(metadata.ref_columns)

    dbt_vars = {
        'source_project': metadata.project_id,
        'source_dataset': metadata.dataset_id
    }
    dbt_vars.update(metadata.spintop_da_vars.as_vars())

    env = OrgDataEnv(
        name=metadata.target['name'],
        vars=dbt_vars
    )

    dataspecs = EnvDataspecs(
        external_project_id=metadata.project_id,
        external_dataset_id=metadata.dataset_id
    )

    transitions_and_nodes_user_fields = (
        metadata.spintop_da_vars.transitions.get('keep_steps_entered_fields', []) + 
        metadata.spintop_da_vars.transitions.get('keep_previous_steps_entered_fields', []) +
        metadata.spintop_da_vars.step_nodes.get('super_group_by_lc_types', []) +
        metadata.spintop_da_vars.step_nodes.get('group_by_lc_types', [])
    )



    dataspecs.production_nodes = TableSpec(
        custom_dimensions=list(
            create_user_fields_dimensions(
                'production_nodes', 
                transitions_and_nodes_user_fields,
                columns
            )
        )
    )

    env.dataspecs = dataspecs
    return env

def index_columns_by_table_name_dot_column_name(ref_columns):
    indexed = {}
    for col in ref_columns:
        indexed[f'{col.table_name}.{col.column_name}'] = col
    return indexed

def create_user_fields_dimensions(table_name, user_fields, columns):
    for user_field in user_fields:
        field_index = f'{table_name}.{user_field}'

        if field_index not in columns:
            pass # No dimensions.
        else:
            col = columns[field_index]
            data_type = col.data_type
            yield from expand_data_type(user_field, data_type)


StructSubType = namedtuple('StructSubType', ['field_name', 'data_type'])
struct_regex = re.compile(r'STRUCT<([\s\S]*)>')
fields_regex = re.compile(r'(?:(\w+) (STRUCT<[\s\S]*>|[\w]+))')
def expand_data_type(field_name, data_type, parent_fields=[]):

    struct_data_type_match = struct_regex.match(data_type.strip())
    if struct_data_type_match:
        # It's a struct.
        fields_str = struct_data_type_match.group(1)
        for match in fields_regex.finditer(fields_str):
            sub_field_name = match.group(1)
            data_type =  match.group(2)
            yield from expand_data_type(sub_field_name, data_type, parent_fields=parent_fields + [field_name])

    elif field_name != '_type':
        yield DimensionSpec(
            name='.'.join(parent_fields + [field_name]),
            field_type=data_type.lower()
        )
