#!/usr/bin/env python3

import argparse
import io
import sys
import simplejson as json
import logging
import collections
import threading
import http.client
import urllib
import pkg_resources


from jsonschema import validate
import singer

from oauth2client import tools
from tempfile import TemporaryFile

import google.auth
from google.cloud import bigquery
from google.cloud.bigquery import Dataset
from google.api_core import exceptions

from .base import BigQueryDictLoadJobBuilder
from .schema import build_schema

from spintop.analytics.singer import parse_message_dict

logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)
logger = singer.get_logger()

SCOPES = ['https://www.googleapis.com/auth/bigquery','https://www.googleapis.com/auth/bigquery.insertdata']
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Singer BigQuery Target'

StreamMeta = collections.namedtuple('StreamMeta', ['schema', 'key_properties', 'bookmark_properties'])

def emit_state(state):
    if state is not None:
        line = json.dumps(state)
        logger.debug('Emitting state {}'.format(line))
        sys.stdout.write("{}\n".format(line))
        sys.stdout.flush()

def clear_dict_hook(items):
    return {k: v if v is not None else '' for k, v in items}

def merge_schemas(*schemas):
    all_fields = collections.OrderedDict()
    for schema in schemas:
        for field in schema:
            key = field.name
            current_field = all_fields.get(key, None)
            if key in all_fields and field != current_field:
                same_fields = False
                if field.field_type == 'RECORD' and current_field.field_type == 'RECORD':
                    # order is not important. compare field by field.
                    same_fields = not bool(
                        set(field.fields).symmetric_difference(set(current_field.fields))
                    )
                
                if not same_fields:
                    raise ValueError(f'Schema type conflict for field {key}: {field} vs {all_fields[key]}')
            all_fields[key] = field
    
    return list(all_fields.values())

class TargetBigQuery(object):
    def __init__(self, bigquery_client, dataset):
        self.bigquery_client = bigquery_client
        self.dataset = dataset

    @classmethod
    def from_project_dataset_id(cls, project_id, dataset_id, job_project_id=None):
        """
        Params:
            project_id: The project where the dataset resiedes.
            dataset_id: The dataset id
            job_project_id (optional): The project where queries will be executed. Uses project_id if not specified.
        """

        if job_project_id is None:
            job_project_id = project_id

        credentials, _ = google.auth.default(
            scopes=[
                "https://www.googleapis.com/auth/drive",
                "https://www.googleapis.com/auth/bigquery",
            ]
        )

        bigquery_client = bigquery.Client(credentials=credentials, project=job_project_id)
        dataset_ref = bigquery_client.dataset(dataset_id, project=project_id)
        dataset = Dataset(dataset_ref)
        return cls(bigquery_client=bigquery_client, dataset=dataset)

    def try_create_dataset(self):
        try:
            dataset = self.bigquery_client.create_dataset(self.dataset)
        except (exceptions.Conflict, exceptions.Forbidden):
            pass

    def persist_lines_job(self, lines=None, truncate=False, validate_records=True):
        messages = []
        for line in lines:
            key = idx # Unique JSON key for the schema possibly
            try:
                msg = singer.parse_message(line)
            except json.decoder.JSONDecodeError:
                logger.error("Unable to parse:\n{}".format(line))
                raise
            
            messages.append(msg)
        return persist_messages_job(messages, truncate=truncate, validate_records=validate_records)

    def persist_messages_job(self, messages=None, truncate=False, validate_records=True):
        state = None
        schemas = {}
        key_properties = {}
        tables = {}
        rows = collections.defaultdict(dict)
        errors = {}
        current_schema_key = None

        bigquery_client = self.bigquery_client
        dataset = self.dataset

        for idx, msg in enumerate(messages):
            key = idx # Unique JSON key for the schema possibly
            if not isinstance(msg, singer.Message):
                msg = parse_message_dict(msg)
            # try:
            #     msg = singer.parse_message(line)
            # except json.decoder.JSONDecodeError:
            #     logger.error("Unable to parse:\n{}".format(line))
            #     raise
            
            if not rows[msg.stream].get(current_schema_key):
                rows[msg.stream][current_schema_key] = BigQueryDictLoadJobBuilder(dataset.dataset_id, msg.stream, truncate=truncate, client=bigquery_client, dataset=dataset)

            job_builder = rows[msg.stream][current_schema_key]

            if isinstance(msg, singer.RecordMessage):
                # if not current_schema_key:
                #     raise Exception("A record for stream {} was encountered before a corresponding schema".format(msg.stream))


                if validate_records and current_schema_key:
                    schema = schemas[current_schema_key]
                    validate(msg.record, schema)

                job_builder.add_row(msg.record)

                state = None

            elif isinstance(msg, singer.StateMessage):
                logger.debug('Setting state to {}'.format(msg.value))
                state = msg.value

            elif isinstance(msg, singer.SchemaMessage):
                table = msg.stream 
                key_properties[table] = msg.key_properties
                
                table_ref = dataset.table(table)
                
                job_builder = rows[msg.stream][current_schema_key]
                current_schema = schemas.get(current_schema_key, None)
                
                if current_schema is None and not truncate:
                    # Get or create from big query
                    try:
                        remote_table = bigquery_client.get_table(table_ref)
                    except exceptions.NotFound:
                        remote_table = bigquery_client.create_table(table_ref)

                    current_schema = remote_table.schema
                    

                if key not in schemas:
                    new_schema = build_schema(msg.schema)
                    if not truncate:
                        merged_schema = merge_schemas(current_schema, new_schema)
                    else:
                        merged_schema = new_schema
                    schemas[key] = merged_schema
                    tables[table] = bigquery.Table(dataset.table(table), schema=merged_schema)

                current_schema_key = key

            elif isinstance(msg, singer.ActivateVersionMessage):
                # This is experimental and won't be used yet
                pass

            else:
                raise Exception("Unrecognized message {}".format(msg))
        
        jobs = []
        for table in rows.keys():
            tables_schemas = rows[table]
            for schema_key in tables_schemas.keys():
                job_builder = tables_schemas[schema_key]
                if not job_builder.is_empty:
                    job_builder.schema = schemas.get(schema_key, None)

                    load_job = job_builder.build_job()
                    jobs.append(load_job)

        for job in jobs:
            result = job.result()
            # logger.info(result)

        # for table in errors.keys():
        #     if not errors[table]:
        #         print('Loaded {} row(s) into {}:{}'.format(rows[table], dataset_id, table), tables[table].path)
        #     else:
        #         print('Errors:', errors[table], sep=" ")

        return state

    def persist_lines_stream(self, project_id, dataset_id, lines=None, validate_records=True):
        raise NotImplementedError()
        state = None
        schemas = {}
        key_properties = {}
        tables = {}
        rows = {}
        errors = {}

        bigquery_client = bigquery.Client(project=project_id)

        dataset_ref = bigquery_client.dataset(dataset_id)
        dataset = Dataset(dataset_ref)
        try:
            dataset = bigquery_client.create_dataset(Dataset(dataset_ref)) or Dataset(dataset_ref)
        except exceptions.Conflict:
            pass

        for line in lines:
            try:
                msg = singer.parse_message(line)
            except json.decoder.JSONDecodeError:
                logger.error("Unable to parse:\n{}".format(line))
                raise

            if isinstance(msg, singer.RecordMessage):
                if msg.stream not in schemas:
                    raise Exception("A record for stream {} was encountered before a corresponding schema".format(msg.stream))

                schema = schemas[msg.stream]

                if validate_records:
                    validate(msg.record, schema)

                errors[msg.stream] = bigquery_client.insert_rows_json(tables[msg.stream], [msg.record])
                rows[msg.stream] += 1

                state = None

            elif isinstance(msg, singer.StateMessage):
                logger.debug('Setting state to {}'.format(msg.value))
                state = msg.value

            elif isinstance(msg, singer.SchemaMessage):
                table = msg.stream 
                schemas[table] = msg.schema
                key_properties[table] = msg.key_properties
                tables[table] = bigquery.Table(dataset.table(table), schema=build_schema(schemas[table]))
                rows[table] = 0
                errors[table] = None
                try:
                    tables[table] = bigquery_client.create_table(tables[table])
                except exceptions.Conflict:
                    pass

            elif isinstance(msg, singer.ActivateVersionMessage):
                # This is experimental and won't be used yet
                pass

            else:
                raise Exception("Unrecognized message {}".format(msg))

        for table in errors.keys():
            if not errors[table]:
                logging.info('Loaded {} row(s) into {}:{}'.format(rows[table], dataset_id, table, tables[table].path))
                emit_state(state)
            else:
                logging.error('Errors:', errors[table])

        return state

def collect():
    try:
        version = pkg_resources.get_distribution('target-bigquery').version
        conn = http.client.HTTPConnection('collector.singer.io', timeout=10)
        conn.connect()
        params = {
            'e': 'se',
            'aid': 'singer',
            'se_ca': 'target-bigquery',
            'se_ac': 'open',
            'se_la': version,
        }
        conn.request('GET', '/i?' + urllib.parse.urlencode(params))
        conn.getresponse()
        conn.close()
    except:
        logger.debug('Collection request failed')

def main():
    try:
        parser = argparse.ArgumentParser(parents=[tools.argparser])
        parser.add_argument('-c', '--config', help='Config file', required=True)
        flags = parser.parse_args()

    except ImportError:
        flags = None

    with open(flags.config) as input:
        config = json.load(input)

    if not config.get('disable_collection', False):
        logger.info('Sending version information to stitchdata.com. ' +
                    'To disable sending anonymous usage data, set ' +
                    'the config parameter "disable_collection" to true')
        threading.Thread(target=collect).start()

    if config.get('replication_method') == 'FULL_TABLE':
        truncate = True
    else:
        truncate = False

    validate_records = config.get('validate_records', True)

    input = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

    if config.get('stream_data', True):
        state = persist_lines_stream(config['project_id'], config['dataset_id'], input, validate_records=validate_records)
    else:
        state = persist_lines_job(config['project_id'], config['dataset_id'], input, truncate=truncate, validate_records=validate_records)

    emit_state(state)
    logger.debug("Exiting normally")


if __name__ == '__main__':
    main()