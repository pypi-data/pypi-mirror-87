from typing import List, Dict, Any
from uuid import uuid4

from spintop.env import SpintopEnv, alias_for
from spintop.messages import SpintopMessagePublisher, Topics
from spintop.models.lifecycles import FileHandlingContext, reserve_lifecycle_streams

from .bootstrap import gcp_bootstrap, no_provider_bootstrap, not_implemented_bootstrap

from .services.dbt_cloud import DbtCloudInterface

class SpintopDeployEnv(SpintopEnv):
    _env_side_input = None

    SPINTOP_DEPLOY_UUID: str = None

    SPINTOP_STAGE: str = 'dev'
    SPINTOP_DATABASE_STAGE: str = 'dev'
    SPINTOP_CLOUD_PROVIDER: str = 'none'

    # GCP
    GOOGLE_CLOUD_PROJECT: str = None
    GOOGLE_CLOUD_REGION: str = None
    GAE_VERSION: str = None # Google App Engine
    PUBSUB_EMULATOR_HOST: str = None # Local emulator if set
    COMMIT_SHA: str = None
    IMPERSONATE_SERVICE_ACCOUNT: str = None
    CLOUD_TASKS_QUEUE_NAME: str = None

    # Dbt Cloud
    DBT_CLOUD_AUTH_TOKEN: str = None
    DBT_INTERFACE_TYPE: str = 'bigquery'

    # Prefect
    PREFECT_PROJECT: str = None
    PREFECT_STORAGE_GCS_BUCKET: str = None
    PREFECT_SERVERLESS_ID_MAP_ENCODED: str = None
    PREFECT_SERVERLESS_TRIGGER_ONLY: bool = False

    @property
    def uuid(self):
        if self.SPINTOP_DEPLOY_UUID is None:
            self.SPINTOP_DEPLOY_UUID = uuid4()
        return str(self.SPINTOP_DEPLOY_UUID)

    def provider_modules(self):
        return ProviderModules(self.deployment_provider_modules().modules)

    def deployment_provider_modules(self):
        providers = {
            'gcp': gcp_bootstrap,
            'aws': not_implemented_bootstrap,
            'none': no_provider_bootstrap
        }
        cloud_provider = self.SPINTOP_CLOUD_PROVIDER
        bootstrap_fn = providers.get(cloud_provider)

        if bootstrap_fn:
            return bootstrap_fn(self)
        else:
            raise ValueError(f'Invalid cloud provider: SPINTOP_CLOUD_PROVIDER={cloud_provider!r}')

    def file_handling_context(self, filename):
        return FileHandlingContext(filename, self)

    def dbt_cloud_factory(self):
        return DbtCloudInterface(self)

    def dbt_interface(self, project_dir, temp_dir=None):
        from .services.dbt_interface import BigqueryOutputFactory, DBTInterface

        output_factories = {
            'bigquery': BigqueryOutputFactory
        }

        factory_cls = output_factories.get(self.DBT_INTERFACE_TYPE, None)
        if not factory_cls:
            raise ValueError(f'Unsupported output factory: {self.DBT_INTERFACE_TYPE}')

        return DBTInterface(
            project_dir=project_dir, 
            output_factory=factory_cls.from_env(self),
            temp_dir=temp_dir
        )

    def prefect_context(self, agent_name=None, param_provider=None):
        from prefect.environments.storage import GCS
        from .prefect_sls.context import SpintopServerlessPrefectContext

        if self.PREFECT_STORAGE_GCS_BUCKET:
            storage = GCS(self.PREFECT_STORAGE_GCS_BUCKET, add_default_labels=False)
        else:
            raise ValueError('PREFECT_STORAGE_GCS_BUCKET must be defined.')
        
        return SpintopServerlessPrefectContext(
            prefect_project=self.PREFECT_PROJECT,
            storage=storage,
            agent_name=agent_name,
            id_map_encoded=self.PREFECT_SERVERLESS_ID_MAP_ENCODED,
            param_provider=param_provider,
            trigger_only=self.PREFECT_SERVERLESS_TRIGGER_ONLY
        )

    def write_prefect_context_id_map(self, context, output_file):
        with open(output_file, 'w+', newline='\n') as source_file:
            source_file.write(f'export PREFECT_SERVERLESS_ID_MAP_ENCODED={context.encode_id_map()}\n')
    

class ProviderModules(object):
    def __init__(self, _modules):
        self._modules = _modules

    def __getattr__(self, name):
        return self._modules[name]

    def get_secret(self, secret_name):
        param_provider = self.param_provider
        return param_provider.get_environ_or_param_value(secret_name)
