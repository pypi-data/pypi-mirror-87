import os

from apache_beam.pipeline import StandardOptions
from apache_beam.options.pipeline_options import GoogleCloudOptions, SetupOptions 

SETUP_FILE = './setup.py'
REQUIREMENTS_FILE = './requirements.txt'

def create_dataflow_options(options, project_id, job_name, setup_file=None, requirements_file=None):
    # if not os.path.exists(SETUP_FILE):
    #     raise RuntimeError(f'Running on dataflow requires the {SETUP_FILE} file.')

    options = options.view_as(GoogleCloudOptions)
    options.project = project_id
    options.job_name = job_name
    options.temp_location = 'gs://nutaq-temp/dataflow-temp'
    options.staging_location = 'gs://nutaq-temp/dataflow-staging'
    options.view_as(StandardOptions).runner = 'DataflowRunner'
    
    if setup_file:
        if not isinstance(setup_file, str):
            # Can be bool
            setup_file = SETUP_FILE
        options.view_as(SetupOptions).setup_file = setup_file
    
    if requirements_file:
        if not isinstance(requirements_file, str):
            # Can be bool
            requirements_file = REQUIREMENTS_FILE
        options.view_as(SetupOptions).requirements_file = requirements_file
