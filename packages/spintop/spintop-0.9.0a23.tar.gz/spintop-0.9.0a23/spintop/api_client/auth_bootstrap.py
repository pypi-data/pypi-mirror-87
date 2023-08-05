import functools

from .base import SpintopAPIClientModule

from ..services.auth0 import Auth0Provider


class NoAuthModule(object):
    def get_auth_headers(self):
        return {}

    def refresh_credentials(self):
        raise NotImplementedError('Cannot refresh credentials without an auth module.')


class SpintopAPIAuthProvider(Auth0Provider):
    def __init__(self, *auth0_args, payload_claims={}, **auth0_kwargs):
        super().__init__(*auth0_args, **auth0_kwargs)
        self.decoder = SpintopAccessTokenDecoder(payload_claims)

    @functools.lru_cache(maxsize=128)
    def get_user_orgs(self, access_token):
        token_payload = self.jwt_verify(access_token)
        return self.decoder.get_user_orgs(token_payload)

class SpintopAccessTokenDecoder(object):
    def __init__(self, payload_claims):
        self.payload_claims = payload_claims
    
    def _claim_name(self, key):
        return self.payload_claims.get(key)

    def get_user_orgs(self, token_payload):
        scopes = token_payload.get('scope').split(' ')
        scopes += token_payload.get('permissions', [])
        # Use set to remove duplicates
        groups_from_scope = {scope.strip('group:') for scope in scopes if scope.startswith('group:')}
        return list(groups_from_scope)

class SpintopAPISpecAuthBootstrap(SpintopAPIClientModule):
    """A no auth client module to bootstrap the retrieval of api spec before the auth_provider exists,
    since its parameters are returned by the /api endpoint itself."""
    def __init__(self, api_url):
        super().__init__(api_url, auth=NoAuthModule())
        self._api_spec = None
        self._auth_provider = None

    @property
    def auth_client_id(self):
        api_spec = self.api_spec
        auth_spec = api_spec['auth']
        return auth_spec.get('machine_client_id')

    def get_auth_spec(self):
        api_spec = self.api_spec
        self.invalidate_api_spec()
        auth_spec = api_spec['auth']
        return dict(
            enabled=auth_spec.get('enabled'),
            domain=auth_spec.get('domain'),
            client_id=auth_spec.get('machine_client_id'),
            audience=auth_spec.get('audience'),
            jwks_url=auth_spec.get('jwks_url'),
            user_info_url=auth_spec.get('user_info_url'),
            payload_claims=auth_spec.get('payload_claims', {})
        )

    def get_auth_provider(self):
        if self._auth_provider is None:
            auth_spec = self.get_auth_spec()
            if auth_spec.pop('enabled'):
                try:
                    self._auth_provider = SpintopAPIAuthProvider(**auth_spec)
                    
                except ValueError:
                    raise ValueError(f'API Spec is invalid: unable to create auth0 provider. {auth_spec}')
        return self._auth_provider
    
    def describe(self):
        return f'User-based bootstrap with client_id={self.auth_client_id} (as prescribed from {self.api_url!r} API spec)'

class BackendSpintopApiAuthProvider(SpintopAPIAuthProvider):
    def refresh_access_token(self, refresh_token=None):
        # Use client credentials grant instead of refreshing token.
        # This requires a client_id and secret_key.
        return self.client_credentials()

class SpintopBackendAPISpecAuthBootstrap(SpintopAPISpecAuthBootstrap):
    def __init__(self, api_url, client_id, secret_key):
        super().__init__(api_url)

        self.client_id = client_id
        self.secret_key = secret_key

    @property
    def auth_client_id(self):
        return self.client_id

    def get_auth_provider(self):
        if self._auth_provider is None:
            auth_spec = self.get_auth_spec()
            auth_spec['client_id'] = self.client_id
            auth_spec['secret_key'] = self.secret_key
            if auth_spec.pop('enabled'):
                try:
                    self._auth_provider = BackendSpintopApiAuthProvider(**auth_spec)
                except ValueError:
                    raise ValueError(f'API Spec is invalid: unable to create auth0 provider. {auth_spec}')
        return self._auth_provider
    
    def describe(self):
        return f'M2M Secret Key bootstrap with client_id={self.client_id}'
    

def create_backend_auth_bootstrap_factory(client_id, secret_key):
    """Create a factory that uses the machine to machine auth flow using the client_id and secret_key."""
    def auth_bootstrap_factory(api_url):
        return SpintopBackendAPISpecAuthBootstrap(api_url, client_id, secret_key)
    
    return auth_bootstrap_factory
