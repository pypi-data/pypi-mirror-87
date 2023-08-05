import os

from spintop_deploy.logs import _logger

logger = _logger('param-provider')
import os

NO_DEFAULT = object()

class BaseParamProvider(object):
    tolerate_defaults = True

    def get_environ_or_param_value(self, environ_name, param_name=None, decrypt=False, default=NO_DEFAULT):
        try:
            return self._get_environ_or_param_value(environ_name, param_name=param_name, decrypt=decrypt)
        except KeyError:
            if self.tolerate_defaults and default is not NO_DEFAULT:
                return default
            else:
                raise

    def _get_environ_or_param_value(self, environ_name, param_name=None, decrypt=False):
        value_from_environ = os.environ.get(environ_name)
        if value_from_environ is None:
            if param_name is None: param_name = environ_name
            return self.get_param_value(param_name, decrypt=decrypt)
        else:
            return value_from_environ

    def get_param_value(self, name, decrypt=False):
        raise NotImplementedError()

class EnvOnlyParamProvider(BaseParamProvider):
    def _get_environ_or_param_value(self, environ_name, param_name=None, decrypt=False):
        return os.environ[environ_name]

class SSMParamProvider(BaseParamProvider):
    """AWS Param provider"""
    
    def __init__(self, region=os.environ.get('AWS_REGION'), enable=True):
        import boto3
        self.ssm = boto3.client('ssm', region_name=region)
        self.enable = enable
    
    @classmethod
    def init(cls, config):
        return cls(
            region=config['AWS_REGION'],
            enable=not config['EMULATE_AWS']
        )
        
    def get_param(self, name, decrypt=False):
        if not self.enable:
            raise Exception('SSM is disabled when emulating AWS.')
        return self.ssm.get_parameter(
            Name=name,
            WithDecryption=decrypt
        )
    
    def get_param_value(self, name, decrypt=False):
        return self.get_param(name, decrypt=decrypt)['Parameter']['Value']
        

class GCPParamProvider(BaseParamProvider):
    
    def __init__(self, project_id, enable=True):
        from google.cloud import secretmanager
        self.client = secretmanager.SecretManagerServiceClient()
        self.enable = enable
        self.project_id = project_id

    def get_param_value(self, name, decrypt=False):
        return self.get_param(name)

    def get_param(self, name):
        if not self.enable:
            raise Exception('GCP Param Provider is disabled.')
        from google.api_core.exceptions import PermissionDenied
        try:
            path = self.client.secret_path(self.project_id, name) + '/versions/latest'
            return self.client.access_secret_version(name=path).payload.data.decode("utf-8")
        except PermissionDenied as e:
            raise KeyError(f'Unable to find secret with key {name}: {str(e)}')
        
    def new_param_version(self, name, value):
        parent_path = self.client.secret_path(self.project_id, name)
        value = value.encode('utf-8')
        self.client.add_secret_version(parent_path, {'data': value})