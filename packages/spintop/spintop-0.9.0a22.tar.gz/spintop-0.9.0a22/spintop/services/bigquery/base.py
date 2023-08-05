#!/usr/bin/env python3

import simplejson as json
from io import BytesIO
from tempfile import TemporaryFile

from google.cloud import bigquery
from google.cloud.bigquery.job import SourceFormat
from google.cloud.bigquery import Dataset, WriteDisposition
from google.cloud.bigquery import LoadJobConfig
from google.api_core import exceptions

from spintop.logs import _logger

logger = _logger('bigquery')

class BigQueryJobBuilder(object):
    def __init__(self, dataset_id, table_name, truncate=False, project_id=None, client=None, dataset=None):
        self.dataset_id = dataset_id
        self.table_name = table_name

        self.truncate = truncate
        self.schema = None

        if client is None:
            client = bigquery.Client(project=project_id)

        if dataset is None:
            dataset = client.dataset(dataset_id)
        
        self.dataset = dataset
        self.client = client

    def _build_job_from_stream(self, file_stream, load_config):
        dataset_ref = self.dataset
        table_ref = dataset_ref.table(self.table_name)

        file_ref = file_stream
        data_bytes = file_ref.tell()
        file_ref.seek(0)
        load_job = self.client.load_table_from_file(
            file_ref, table_ref,
            job_config=load_config
        )
        logger.info(f'Created job {load_job.job_id} of {data_bytes/1000000} MBytes')
        return load_job

class BigQueryDictLoadJobBuilder(BigQueryJobBuilder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = TemporaryFile(mode='w+b')

    def add_row(self, row_dict):
        dat = bytes(json.dumps(row_dict) + '\n', 'UTF-8')
        self.data.write(dat)

    def add_rows(self, rows):
        for row in rows:
            self.add_row(row)
    
    @property
    def is_empty(self):
        return self.data.tell() == 0
 
    def build_job(self):
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

        return self._build_job_from_stream(self.data, load_config)

class BigQueryParquetLoadJobBuilder(BigQueryDictLoadJobBuilder):

    def set_bytes_stream(self, data):
        self.data = data

    def build_job(self):
        load_config = LoadJobConfig()

        load_config.source_format = SourceFormat.PARQUET
    
        if self.truncate:
            load_config.write_disposition = WriteDisposition.WRITE_TRUNCATE
        else:
            # Allow field addition or relaxation if not truncate.
            load_config.schema_update_options = [
                bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION,
                bigquery.SchemaUpdateOption.ALLOW_FIELD_RELAXATION
            ]

        return self._build_job_from_stream(self.data, load_config)

    