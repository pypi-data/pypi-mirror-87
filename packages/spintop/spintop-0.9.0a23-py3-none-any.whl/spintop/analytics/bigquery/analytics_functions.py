import os
import itertools
import datetime as dt
import hashlib

from google.cloud import bigquery

from jinja2 import Environment, FileSystemLoader, PrefixLoader

from spintop.models import Filter, QueryResult
from spintop.logs import _logger

from ..base import get_uuid_datetime

HERE = os.path.abspath(os.path.dirname(__file__))

logger = _logger('bq-analytics')

def create_dataset_functions(analytics_target):
    bigquery_client = analytics_target.target_bigquery.bigquery_client
    dataset = analytics_target.target_bigquery.dataset

    return BigQueryDatasetFunctions(bigquery_client, dataset)

DEFAULT_SELECT_FIELDS = [
    '* EXCEPT (_type)'
]

class BigQueryDatasetFunctions(object):
    def __init__(self, client, dataset):
        self.client = client
        self.dataset = dataset

        self._existing_tables = None

        self._loaders = {
            'core': FileSystemLoader(os.path.join(HERE, 'queries'))
        }

        self.queries = Environment(
            trim_blocks=True,
            lstrip_blocks=True,
            loader=PrefixLoader(self._loaders)
        )

    @property
    def datatransfer_parent_path(self):
        return self.datatransfer_client.project_path(self.client.project) 

    def add_template_loader(self, key, loader):
        self._loaders[key] = loader

    def map_stream_to_latest_views(self, stream_table, extract_tags=[]):
        return self.render_template('core/stream_to_last.bql', 
            from_table=self.fully_qual_table_name(stream_table),
            extract_tags=extract_tags
        )

    def helper_functions(self):
        return self.render_template('core/create_helper_functions.bql')

    def lc_unit_yields(self, origin_table, lc_type, partition_by=(), select_fields=None):
        partition_by = ('unit.id',) + tuple(partition_by)
        if select_fields is None:
            select_fields = DEFAULT_SELECT_FIELDS
            
        return self.render_template('core/lc_unit_yields.bql',
            from_table=self.fully_qual_table_name(origin_table),
            lc_type=lc_type,
            partition_by=partition_by,
            select_fields=select_fields
        )

    def lc_multi_transitions(self, origin_table, group_by_lc_types=('step',)):
        return self.render_template('core/multi_transitions.bql',
            from_table=self.fully_qual_table_name(origin_table),
            group_by_lc_types=group_by_lc_types
        )

    def stored_query(self, project_id, dataset, query_name, params={}, queries_table='queries'):
        return self.render_template('core/execute_stored_query.bql',
            project_id=project_id,
            dataset=dataset,
            queries_table=queries_table,
            query_name=query_name,
            params=params
        )

    def retrieve_one_uuid_partition(self, project_id, dataset, from_table, uuid, columns=None, input_safe=False):
        uuid_datetime = get_uuid_datetime(uuid)
        DATE_FORMAT = '%Y-%m-%d'
        
        table_schema = None

        if columns is None:
            # uuid is passed as a query param, so no chance of sql injection.
            input_safe = True

        if not input_safe:
            table_name = fully_qual_table_name(project_id, dataset, from_table)
            table = self.client.get_table(table_name)
            table_schema = table.schema

        if columns:
            columns = safe_columns(columns, table_schema=table_schema)

        return self.render_template('core/retrieve_one_uuid_partition.bql',
            from_table=fully_qual_table_name(project_id, dataset, from_table),
            query_params={'uuid': ('STRING', uuid)},
            lower_date_iso=uuid_datetime.strftime(DATE_FORMAT),
            upper_date_iso=(uuid_datetime + dt.timedelta(days=1)).strftime(DATE_FORMAT),
            columns=columns
        )

    def select_many_filtered_ordered(self, project_id, dataset, from_table, filters=[], order_by=[], columns=None, limit_rows=None, input_safe=False):
        table_schema = None

        if not input_safe:
            table_name = fully_qual_table_name(project_id, dataset, from_table)
            table = self.client.get_table(table_name)
            table_schema = table.schema

        if columns:
            columns = safe_columns(columns, table_schema=table_schema)

        if order_by:
            order_by = spintop_order_by_to_bq(order_by, table_schema=table_schema)

        bq_filters, query_params = spintop_filters_to_bq(filters, table_schema=table_schema)

        return self.render_template('core/select_many_filtered_ordered.bql',
            from_table=table_name,
            query_params=query_params,
            filters=bq_filters,
            order_by=order_by,
            columns=columns,
            limit_rows=limit_rows
        )

    def measure_values_mart(self, origin_table, measure_names={}, column=None):
        if column is None:
            column = 'value_f'
        if measure_names:
            return self.render_template('core/measures_mart.bql', 
                from_table=self.fully_qual_table_name(origin_table), 
                measure_names=measure_names,
                column=column
            )
        else:
            logger.info('Skipped measure mart because measure names are empty.')

    def array_measure_declarative_values_mart(self, origin_table, declarative_measures={}):
        """
        Declarative measures are of style
        
        # yaml
        ---
        Harmonics:
            keys: 
                freq: [70, 200, 1000, 2000, 3000]
                tx: [1, 2, 3, 4]
            name_format: 'Tx{tx}_{freq}MHz_Harmonic2'
        
        """
        return self.array_measure_values_mart(origin_table,
            measures=array_measure_generator_from_declarative(declarative_measures)
        )

    def array_measure_values_mart(self, origin_table, measures={}):
        """
        Normal array measures are of style

        # yaml
        ---
        Harmonics:
          - name: 'Tx{tx}_{freq}MHz_Harmonic2'
            keys:
              - freq: 70
                tx: 1
              - freq: 70
                tx: 2
              - ...
            value_column: value_f
        """
        if measures:
            return self.render_template('core/array_measures_mart.bql', 
                from_table=self.fully_qual_table_name(origin_table), 
                measures=measures
            )
        else:
            logger.info('Skipped array measure mart because measures are empty.')

    def list_tables(self):
        if not self._existing_tables:
            self._existing_tables = {table.table_id: table for table in self.client.list_tables(self.dataset)}
        return self._existing_tables

    def table_exists(self, table_name):
        dataset_tables = self.list_tables() 
        table_ref = dataset_tables.get(table_name, None)
        return table_ref is not None

    def create_empty_table(self, table_name):
        table_name = self.fully_qual_table_name(table_name)
        table = bigquery.Table(table_name)
        table = self.client.create_table(table)  # Make an API request.

    def render_template(self, query_template, query_params={}, **template_kwargs):
        template = self.queries.get_template(query_template)
        query = template.render(repr=repr, fully_qual_table_name=self.fully_qual_table_name, **template_kwargs)
        return self.prepare_query(query, name=query_template, query_params=query_params)

    def prepare_query(self, query, name=None, query_params={}):
        return PreparedQuery(query, self, name=name, params=query_params)

    def update_view(self, table_name, prepared_query):
        logger.info(f'Updating view {prepared_query} to {table_name!r}')

        query = prepared_query.query
        dataset_tables = self.list_tables() 
        table_ref = dataset_tables.get(table_name, None)

        exists = False
        update = False

        if table_ref:
            # Exists
            exists = True
            view = self.client.get_table(table_ref)

            if view.view_query != query:
                logger.info(f'View table {table_name!r} exists but query does not match; will update.')
                update = True
        else:
            # Does not exists.
            logger.info(f'View table {table_name!r} does not exist; will create.')
            exist = False
            update = True
            view_ref = self.dataset.table(table_name)
            view = bigquery.Table(view_ref)

        if update:
            view.view_query = query
            try:
                if exists:
                    self.client.update_table(view, ["view_query"])
                else:
                    self.client.create_table(view)
            except:
                logger.error(f'View with query \n {query} \n failed.', exc_info=True)
                raise

    def materialize_query(self, table_name, prepared_query):
        logger.info(f'Materializing {prepared_query} to {table_name!r}')

        query = prepared_query.query
        
        dataset_tables = self.list_tables() 
        table_ref = dataset_tables.get(table_name, None)

        if table_ref:
            logger.info(f'Table exists, dropping.')

        job_config = bigquery.QueryJobConfig(destination=self.fully_qual_table_name(table_name))
        job_config.write_disposition = "WRITE_TRUNCATE"
        # Start the query, passing in the extra configuration.
        logger.info(f'View will be updated; will not wait for query to end.')
        query_job = self.client.query(query, job_config=job_config)  # Make an API request.
        # query_job.result()  # Wait for the job to complete.
        return query_job

    def execute_query(self, prepared_query):
        logger.info(f'Executing {prepared_query}')

        query = prepared_query.query
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter(param_name, param_type, value)
                for param_name, (param_type, value) in prepared_query.params.items()
            ]
        )

        query_job = self.client.query(query, job_config=job_config)  # Make an API request.
        return BigQueryResult(query_job, self.client)

    def fully_qual_table_name(self, table_name):
        return fully_qual_table_name(self.dataset.project, self.dataset.dataset_id, table_name)

    def create_gsheets_table(self, table_name, sheet_uri, schema, skip_leading_rows=0, sheet_range=None):
        logger.info(f'Creating external sheets source table {table_name}')

        dataset_tables = self.list_tables() 
        table_ref = dataset_tables.get(table_name, None)

        if table_ref:
            logger.info(f'Table exists, dropping.')
            self.client.delete_table(table_ref)  # Make an API request.

        table = bigquery.Table(self.fully_qual_table_name(table_name), schema=schema)
        external_config = bigquery.ExternalConfig("GOOGLE_SHEETS")
        external_config.source_uris = [sheet_uri]
        external_config.options.skip_leading_rows = skip_leading_rows
        external_config.options.range = sheet_range
        table.external_data_configuration = external_config

        return self.client.create_table(table)

def fully_qual_table_name(project_id, dataset_id, table_name):
    return '.'.join([project_id, dataset_id, table_name])

class PreparedQuery(object):
    def __init__(self, query, functions, name=None, params={}):
        self.query = query
        self.functions = functions
        self.name = name
        self.params = params

    def update_view(self, table_name):
        return self.functions.update_view(table_name, self)
    
    def materialize_query(self, table_name):
        return self.functions.materialize_query(table_name, self)

    def execute_query(self):
        return self.functions.execute_query(self)

    def __str__(self):
        name = self.name

        if not name:
            name = (self.query[:75] + '..') if len(self.query) > 77 else self.query
        
        return f'{self.__class__.__name__}({name})'

class BigQueryResult(object):
    def __init__(self, query_job, client):
        self.client = client
        self.query_job = query_job

    def __iter__(self):
        return iter(self.query_job)

    # def list_rows(self, max_results=None):
    #     destination_id = self.query_job.destination

    #     self.query_job.result() # Wait for it to end before retrieving results.
    #     destination = self.client.get_table(destination_id)
    #     iterator = 
    #     for row in self.client.list_rows(destination, max_results=max_results):
    #         yield dict(row)

    def as_query_result(self, max_results=None):
        destination_id = self.query_job.destination

        self.query_job.result() # Wait for it to end before retrieving results.

        # Is this necessary ? API call
        # destination = self.client.get_table(destination_id)
        destination = self.query_job.destination

        row_iterator = self.client.list_rows(destination, max_results=max_results)
        rows = [dict(row) for row in row_iterator]
        return QueryResult(
            query_id=self.query_job.etag,
            total_rows_count=row_iterator.total_rows,
            rows_count=len(rows),
            page_token=None,
            next_page_token=None,
            rows=rows
        )

def array_measure_generator_from_declarative(definition):
    generated_def = {}

    for key, value in definition.items():
        name_format = value['name_format']
        declarative_keys = value['keys']
        
        keys, values = zip(*declarative_keys.items())
        
        listed_keys = [
            dict(zip(keys, bundle)) for bundle in itertools.product(*values)
        ]

        generated_def[key] = {
            'name': name_format,
            'keys': listed_keys,
            'value_column': value.get('value_column', 'value_f')
        }

    return generated_def

def check_schema_has_field_name(schema, field_name, path=[]):
    field_name_parts = field_name.split('.')
    field_name = field_name_parts[0]
    other_parts = field_name_parts[1:]

    if field_name == '*':
        return True

    found_field = None
    for field in schema:
        if field.name == field_name:
            found_field = field
            break
    else:
        raise ValueError(f'Schema does not have a field named {".".join(path + [field_name])}')

    if found_field.field_type == 'RECORD':
        if other_parts:
            return check_schema_has_field_name(found_field.fields, '.'.join(other_parts), path=path+[field_name])
        else:
            return True # Asked for this record explicitely
    elif other_parts:
        raise ValueError(f'Sub field is not of type records but sub keys were specified.')
    else:
        return True


def spintop_filters_to_bq(filters, table_schema=None):
    OP_MAP = {
        'eq': _bq_simple_operator('='),
        'neq': _bq_simple_operator('!='),
        'lt': _bq_simple_operator('<'),
        'lte': _bq_simple_operator('<='),
        'gt': _bq_simple_operator('>'),
        'gte': _bq_simple_operator('>='),
        'match': None,
        'search': bq_regex_search
    }

    bq_filters = []
    params = {}

    for f in filters:
        if table_schema:
            check_schema_has_field_name(table_schema, f.name)
        
        # Creates an md5 hash of this string to use as an identifer for the @x notation of BigQuery parameters.
        internal_name = safe_identifier(f.name + '/' + f.op)

        field_type = f.field_type
        if field_type == 'datetime':
            field_type = 'timestamp'

        field_type = field_type.upper()
        params[internal_name] = (field_type, f.val)
        op = OP_MAP.get(f.op)

        bq_filters.append(op(f.name, field_type, internal_name))
    
    return bq_filters, params
            

def bq_regex_search(field_name, field_type, internal_name):
    return f'REGEXP_CONTAINS(CAST({field_name} AS {field_type}), CAST(@{internal_name} AS {field_type}))'

def _bq_simple_operator(op):
    return lambda field_name, field_type, internal_name: f'CAST({field_name} AS {field_type}) {op} CAST(@{internal_name} AS {field_type})'

def safe_identifier(field_name):
    result = hashlib.md5(field_name.encode())
    return '_' + result.hexdigest()

def safe_columns(columns, table_schema=None):

    for column in columns:
        if table_schema:
            check_schema_has_field_name(table_schema, column)

    return columns

def spintop_order_by_to_bq(order_bys, table_schema=None):

    bq_order_by = []

    for order_by in order_bys:
        if table_schema:
            check_schema_has_field_name(table_schema, order_by.name)
        
        asc_or_desc = 'ASC' if order_by.asc else 'DESC'
        bq_order_by.append(f'{order_by.name} {asc_or_desc}')
    
    return bq_order_by