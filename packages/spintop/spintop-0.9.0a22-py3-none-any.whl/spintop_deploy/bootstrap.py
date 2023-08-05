""" This is the 'meta' config module. Based on environ, decide on the best config object, param provider, and deployment type."""
import os

from incremental_module_loader import IncrementalModuleLoader

from spintop import __version__ as spintop_version

from .logs import _logger

try:
    from opencensus.ext.stackdriver import trace_exporter as stackdriver_exporter
    def initialize_gcp_tracer_export(project_id):
        exporter = stackdriver_exporter.StackdriverExporter(
            project_id=project_id
        )
        return exporter
except ImportError:
    initialize_gcp_tracer_export = lambda: None

logger = _logger('config-factory')

def no_provider_bootstrap(env, _modules=None):
    from .services.param_provider import EnvOnlyParamProvider
    _modules = _common_bootstrap(env, _modules)
    _modules.load(param_provider=EnvOnlyParamProvider)
    return _modules

def gcp_bootstrap(env, _modules=None):
    _modules = _common_bootstrap(env, _modules)
    _modules.load(_gcp_bootstrap)
    return _modules

def not_implemented_bootstrap(env, _modules=None):
    raise NotImplementedError()

def _common_bootstrap(env, _modules=None):
    if _modules is None:
        _modules = IncrementalModuleLoader()

    _modules.update(_modules=_modules, env=env)
    
    deployment_config = dict(
        _provider=None,
        _force_enable_auth=False,
        version=None,
        stage=None
    )

    stage = env.SPINTOP_STAGE
    db_stage = env.SPINTOP_DATABASE_STAGE

    for _stage in (stage, db_stage):
        if _stage not in ['prod', 'dev', 'test', 'staging']:
            raise ValueError(f'Invalid stage name: {_stage!r}')
    
    deployment_config['stage'] = stage
    deployment_config['db_stage'] = db_stage
    deployment_config['_provider'] = env.SPINTOP_CLOUD_PROVIDER

    _modules.update(
        deployment_config=deployment_config,
        versions=dict(
            spintop=spintop_version
        )
    )
    return _modules

def _gcp_bootstrap(env, deployment_config, _modules=None):
    from .services.param_provider import GCPParamProvider
    from .services.pub_sub import GCPPubSub
    from .services.cloud_tasks import GoogleCloudTaskQueue
    from spintop.services.analytics_provider import BigQueryAnalyticsProvider

    project_id = env.GOOGLE_CLOUD_PROJECT
    pub_sub_emulator = env.PUBSUB_EMULATOR_HOST

    deployment_config['version'] = env.GAE_VERSION
    deployment_config['pubsub_emulator'] = pub_sub_emulator is not None
    deployment_config['_force_enable_auth'] = True

    deployment_config['_gcp'] = {
        'project_id': project_id
    }
    
    _modules.update(
        project_id=project_id, 
        gcp_region=env.GOOGLE_CLOUD_REGION, 
        gcp_queue_name=env.CLOUD_TASKS_QUEUE_NAME, 
        impersonate_service_account=env.IMPERSONATE_SERVICE_ACCOUNT
    )

    _modules.load(param_provider=GCPParamProvider)
    if deployment_config['stage'] in ['prod', 'staging']:
        # No defaults tolerated when running in prod or staging.
        # Avoids accidental default secret key values for example.
        _modules['param_provider'].tolerate_defaults = False

    _modules.load(pub_sub=GCPPubSub)
    _modules.load(tracer_export=initialize_gcp_tracer_export)
    _modules.load(analytics_provider=BigQueryAnalyticsProvider)
    _modules.load(task_queue=GoogleCloudTaskQueue)
    return _modules