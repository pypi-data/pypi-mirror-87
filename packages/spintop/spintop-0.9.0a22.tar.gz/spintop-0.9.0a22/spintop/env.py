import os
from dataclasses import dataclass

from .api_client import (
    SpintopAPIClientModule, 
    SpintopAPISpecAuthBootstrap, 
    create_backend_auth_bootstrap_factory, 
    SpintopAPIPersistenceFacade, 
    SpintopAPIAnalytics
)

from .auth import FilePathCredentialsStore
from .spintop import SpintopFactory

from .storage import SITE_DATA_DIR
from .messages import LocalMessagePublisher, SpintopMessagePublisher
from .analytics.base import sanitize_key

from .analytics.contextual import ContextualAnalyticsTarget

def alias_for(env_name):
    return property(
        fget= lambda env: env[env_name],
        fset= lambda env, value: env.__setitem__(env_name, value)
    )

NO_VALUE = object()

def Spintop(api_url=None, org_id=None, verbose=False, init_env={}):
    env = SpintopEnv(init_env, verbose=verbose, api_url=api_url, org_id=org_id)
    return env.spintop_factory()

def _api_analytics():
    return SpintopAPIAnalytics

def _bigquery_analytics():
    from .analytics.bigquery import AdvancedBigQueryAnalytics
    return AdvancedBigQueryAnalytics
    
class SpintopEnv():
    # Credentials file is used to store access and refresh tokens.
    SPINTOP_CREDENTIALS_FILE: str = os.path.join(SITE_DATA_DIR, '.spintop-credentials.yml')

    # Client id and secret is used for machine to machine auth flow.
    SPINTOP_M2M_CLIENT_ID: str = None
    SPINTOP_M2M_SECRET_KEY: str = None

    SPINTOP_PERSISTENCE_TYPE: str = 'api'

    # used if SPINTOP_PERSISTENCE_TYPE is 'api'
    SPINTOP_API_URI: str = 'https://cloud.spintop.io'

    # used if SPINTOP_PERSISTENCE_TYPE is 'none' (placeholder)
    SPINTOP_NONE_URI: str = None

    # used if SPINTOP_PERSISTENCE_TYPE is 'mongo'
    SPINTOP_MONGO_URI: str 

    # used if SPINTOP_PERSISTENCE_TYPE is 'postgres'
    SPINTOP_POSTGRES_URI: str

    # used by all persistence types
    SPINTOP_DATABASE_NAME: str = None

    # Analytics
    SPINTOP_ANALYTICS_TYPE: str = 'api'

    # The dataset full path
    SPINTOP_BIGQUERY_URI: str = None 

    # other
    SPINTOP_VERBOSE: bool = False

    # GCP
    GOOGLE_CLOUD_PROJECT: str = None

    # Aliases for python-friendly attributes
    api_url = alias_for('SPINTOP_API_URI') # URL
    api_uri = alias_for('SPINTOP_API_URI') # URI

    credentials_filepath = alias_for('SPINTOP_CREDENTIALS_FILE')
    org_id = alias_for('SPINTOP_DATABASE_NAME')
    verbose = alias_for('SPINTOP_VERBOSE')
    database_name = alias_for('SPINTOP_DATABASE_NAME')

    # Can be replaced/extended by sub classes.
    ANALYTICS_CLS_BY_TYPE = {
        'bigquery': _bigquery_analytics,
        'api': _api_analytics,
    }

    def __init__(self, _init_values=None, verbose=False, api_url=None, org_id=None, ignore_invalid_init_value=False):
        if _init_values is None:
            _init_values = {}

        # Replace default values by possible a real env value.
        for key in self.ENV_NAMES:
            default_value = NO_VALUE
            if hasattr(self, key):
                default_value = self[key]

            setattr(self, key, os.environ.get(key, default_value))

        for key, value in _init_values.items():
            try:
                self[key] = value # Will validate if key is part of the support env variables.
            except KeyError:
                if not ignore_invalid_init_value:
                    raise

        if api_url:
            # for some reason, the requests module adds 1 second to every request made using localhost
            # replacing it with 127.0.0.1 removes this strange issue.
            self.api_url = api_url.replace('//localhost', '//127.0.0.1') 
        
        if org_id:
            self.org_id = org_id

        self.verbose = verbose

    @property
    def ENV_NAMES(self):
        annotations = {}
        for cls in self.__class__.__mro__:
            annotations.update(cls.__dict__.get('__annotations__', {}))
        return list(annotations.keys())

    def __getattr__(self, key):
        """When an attribute does not exist, attempt to retrieve it from env."""
        try:
            self._must_be_an_env_key(key)
            return os.environ[key]
        except KeyError as e:
            # Raise as attribute error for __getattr__ 
            raise AttributeError(str(e))

    def __getitem__(self, key):
        self._must_be_an_env_key(key)
        value = getattr(self, key)
        if value is NO_VALUE:
            raise KeyError(key)
        return value
    
    def __setitem__(self, key, value):
        self._must_be_an_env_key(key)
        setattr(self, key, value)

    def get(self, key, default_value=None):
        try:
            return self[key]
        except:
            return default_value

    def _must_be_an_env_key(self, key):
        if key not in self.ENV_NAMES:
            raise KeyError(f'{key!r} is not a SpintopEnv variable.')

    def freeze(self, specific_keys=None):
        if not specific_keys: 
            specific_keys = self.ENV_NAMES
        return {key: self.get(key) for key in specific_keys}

    def freeze_database_access_only(self):
        keys = [
            'SPINTOP_PERSISTENCE_TYPE',
            self._facade_uri_env_name(self.SPINTOP_PERSISTENCE_TYPE),
            'SPINTOP_DATABASE_NAME'
        ]
        return self.freeze(keys)

    def copy(self, **new_env_values):
        new_env = self.__class__(self.freeze())
        for key, value in new_env_values.items():
            new_env[key] = value
        return new_env

    def new_database_context(self, database_name):
        env = self.copy()
        env.database_name = database_name
        return env

    def get_facade_uri(self, facade_type=None):
        return self[self._facade_uri_env_name(facade_type)]

    def transform_facade_uri(self, transform, facade_type=None):
        key_name = self._facade_uri_env_name(facade_type)
        self[key_name] = transform(self[key_name])

    def _facade_uri_env_name(self, facade_type=None):
        if facade_type is None: facade_type = self.SPINTOP_PERSISTENCE_TYPE
        return f'SPINTOP_{facade_type.upper()}_URI'

    def get_persistence_cls(self, facade_type=None):
        if facade_type is None: facade_type = self.SPINTOP_PERSISTENCE_TYPE
        facade_cls_by_type = {
            'mongo': _mongo_facade,
            'postgres': _postgresql_facade,
            'api': _api_facade,
            'none': _not_implemented_facade
        }

        if facade_type not in facade_cls_by_type:
            raise ValueError(f'Unknown facade type SPINTOP_PERSISTENCE_TYPE={facade_type!r}. Available: {list(facade_cls_by_type.keys())!r}')
        
        return facade_cls_by_type[facade_type]()

    def get_persistence_params(self, facade_type=None):
        if facade_type is None: facade_type = self.SPINTOP_PERSISTENCE_TYPE
        return dict(
            uri=self.get_facade_uri(facade_type),
            database_name=self.database_name # shared by all
        )

    def _env_persistence_facade_factory(self, spintop_api, message_publisher:SpintopMessagePublisher =None):
        cls = self.get_persistence_cls()
        params = dict(
            spintop_api=spintop_api,
            message_publisher=message_publisher,
            **self.get_persistence_params()
        )
        return cls(**params)

    def persistence_facade_factory(self, message_publisher:SpintopMessagePublisher =None, facade_type=None):
        facade_cls = self.get_persistence_cls(facade_type)
        persistence_params = self.get_persistence_params(facade_type)
        facade = facade_cls(
            env=self,
            **persistence_params
        )
        if message_publisher is not None:
            facade.messages = message_publisher
        return facade
    
    def postgres_sql_ops_factory(self):
        from .persistence.postgresql import engine_from_uri, SQLOperations
        uri = self.get_facade_uri('postgres')
        engine = engine_from_uri(uri, database_name=self.database_name)
        return SQLOperations(engine)

    def get_analytics_cls(self, analytics_type=None):
        if analytics_type is None:
            analytics_type = self.SPINTOP_ANALYTICS_TYPE

        if analytics_type not in self.ANALYTICS_CLS_BY_TYPE:
            raise ValueError(f'Unknown analytics type SPINTOP_ANALYTICS_TYPE={analytics_type!r}. Available: {list(analytics_cls_by_type.keys())!r}')
        
        return self.ANALYTICS_CLS_BY_TYPE[analytics_type]()

    def contextual_analytics_factory(self, *args, spintop_api=None, **kwargs):
        analytics = self.analytics_factory(*args, spintop_api=spintop_api, **kwargs)
        context_analytics = ContextualAnalyticsTarget(analytics)

        if spintop_api:
            spintop_api.register_analytics(context_analytics)

        reserve_lifecycle_streams(context_analytics, self)

        return context_analytics

    def analytics_factory(self, analytics_type=None, spintop_api=None):
        cls = self.get_analytics_cls(analytics_type)
        params = self.get_analytics_params(analytics_type)
        return cls(
            env=self,
            spintop_api=spintop_api,
            **params
        )

    def _env_analytics_factory(self, spintop_api):
        return self.analytics_factory(spintop_api=spintop_api)

    def get_analytics_params(self, analytics_type=None):
        if analytics_type is None:
            analytics_type = self.SPINTOP_ANALYTICS_TYPE
        params = dict(
            uri=self.get_facade_uri(analytics_type),
            database_name=sanitize_key(self.database_name) if self.database_name else None # shared by all
        )
        return params

    def spintop_factory(self, org_id=None, api_url=None, **kwargs):
        if self.SPINTOP_M2M_CLIENT_ID:
            # Use machine to machine auth bootstrap.
            auth_bootstrap_factory = create_backend_auth_bootstrap_factory(self.SPINTOP_M2M_CLIENT_ID, self.SPINTOP_M2M_SECRET_KEY)
        else:
            # Uses the normal user based authentication flow.
            auth_bootstrap_factory = SpintopAPISpecAuthBootstrap

        message_publisher = LocalMessagePublisher(self)

        if org_id is None:
            org_id = self.org_id
        
        if api_url is None:
            api_url = self.api_url

        return SpintopFactory(
            api_url=api_url,
            verbose=self.verbose,
            credentials_filepath=self.credentials_filepath,
            org_id=org_id,
            auth_bootstrap_factory=auth_bootstrap_factory,
            message_publisher=message_publisher,
            persistence_facade_factory=self._env_persistence_facade_factory,
            analytics_factory=self._env_analytics_factory,
            **kwargs
        )

def _not_implemented_facade():
    from .persistence.base import NotImplementedPersistenceFacade
    return NotImplementedPersistenceFacade

def _api_facade():
    return SpintopAPIPersistenceFacade

def _postgresql_facade():
    from .persistence.postgresql import PostgreSQLPersistenceFacade
    return PostgreSQLPersistenceFacade

def _mongo_facade():
    from .persistence.mongo import MongoPersistenceFacade
    return MongoPersistenceFacade