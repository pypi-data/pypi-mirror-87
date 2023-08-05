#!/usr/bin/env python3

import simplejson as json

from tempfile import TemporaryFile

from google.cloud import bigquery
from google.cloud.bigquery.job import SourceFormat
from google.cloud.bigquery import Dataset, WriteDisposition
from google.cloud.bigquery import LoadJobConfig
from google.api_core import exceptions

from spintop.logs import _logger

logger = _logger('bigquery')

class BigQueryDictLoadJobBuilder(object):
    def __init__(self, dataset_id, table_name, truncate=False, project_id=None, client=None):
        self.dataset_id = dataset_id
        self.table_name = table_name

        self.truncate = truncate
        self.schema = None
        self.data = TemporaryFile(mode='w+b')

        if client is None:
            client = bigquery.Client(project=project_id)
        
        self.client = client
    
    def add_row(self, row_dict):
        dat = bytes(json.dumps(row_dict) + '\n', 'UTF-8')
        self.data.write(dat)

    def add_rows(self, rows):
        for row in rows:
            self.add_row(row)
    
    def build_job(self):
        dataset_ref = self.client.dataset(self.dataset_id)

        try:
            dataset = self.client.create_dataset(Dataset(dataset_ref)) or Dataset(dataset_ref)
        except exceptions.Conflict:
            pass

        table_ref = dataset_ref.table(self.table_name)

        load_config = LoadJobConfig()
        if self.schema is None:
            # No schema. Use Bigquery auto schema
            load_config.autodetect = True
        else:
            load_config.schema = self.schema

        load_config.source_format = SourceFormat.NEWLINE_DELIMITED_JSON
    
        if self.truncate:
            load_config.write_disposition = WriteDisposition.WRITE_TRUNCATE
        else:
            # Allow field addition or relaxation if not truncate.
            load_config.schema_update_options = [
                bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION,
                bigquery.SchemaUpdateOption.ALLOW_FIELD_RELAXATION
            ]
        
        file_ref = self.data
        logger.info(f'Creating job of {file_ref.tell()/1000000} MBytes')
        file_ref.seek(0)
        return self.client.load_table_from_file(
            file_ref, table_ref,
            job_config=load_config
        )
