import click
import webbrowser
from contextlib import contextmanager

from pprint import pprint

from ..errors import SpintopException, AuthUnauthorized, ExpiredAccessToken
from .schemas import credentials_schema

class AuthException(SpintopException):
    pass

REFRESH_MODULE = 'user'



class AuthModule(object):
    scopes = ['offline_access', 'openid', 'email', 'profile', 'authorization']
    def __init__(self, auth_bootstrap, credentials_store):
        self._auth_provider_accessor = auth_bootstrap.get_auth_provider if auth_bootstrap else None
        self._auth_bootstrap = auth_bootstrap
        self.credentials_store = credentials_store
        self._reset_credentials()

    @property
    def credentials(self):
        self._init_check()
        return self._credentials
    
    @credentials.setter
    def credentials(self, value):
        self._credentials = value
    
    @property
    def user_orgs(self):
        self.assert_credentials()
        access_token = self.credentials.get('access_token', None)
        if access_token:
            return self.attempt_op_with_refresh(lambda: self.auth_provider.get_user_orgs(access_token))
        else:
            return []

    @property
    def auth_provider(self):
        if callable(self._auth_provider_accessor):
            auth_provider = self._auth_provider_accessor()
        else:
            auth_provider = self._auth_provider_accessor
        return auth_provider

    @auth_provider.setter
    def auth_provider(self, value):
        self._auth_provider_accessor = value

    @property
    def auth_client_id(self):
        return self._auth_bootstrap.auth_client_id

    def _reset_credentials(self):
        self._credentials = None
        self._initialized = False

    def _init_check(self):
        if not self._initialized and not self._credentials:
            self.credentials = self.credentials_store.retrieve()

            if self._credentials is None or not self.credentials_match_auth_provider():
                try:
                    self.refresh_credentials()
                except AuthException:
                    pass
            # Other init stuff should go here
            self._initialized = True
    
    def assert_credentials(self):
        if not self.credentials:
            raise AuthException("No credentials available. Please login.")
    
    def assert_no_login(self):
        if self.credentials:
            raise AuthException(
                f"You already have credentials stored for {self.credentials['username']}. "
                "Spintop currently only support a single user per PC. "
                "Please logout before logging back in."
            )

    @contextmanager
    def login_device_flow(self, scopes=[]):
        self.assert_no_login()
        device_flow = self.auth_provider.DeviceAuthorizationFlow()
        response = device_flow.request_verification_url(scopes=self.scopes + scopes)
        yield response
        webbrowser.open(response.verification_uri_complete, new=2)
        content = device_flow.wait_for_approval()
        user_info = self.auth_provider.get_user_info(content['access_token'])
        self._save_access_token(content, username=user_info['email'])

    def get_user_info(self):
        self.assert_credentials()
        return self.auth_provider.get_user_info(self.credentials['access_token'])

    def login_user_pass(self, username, password, scopes=[]):
        self.assert_no_login()
        content = self.auth_provider.authenticate(username, password, scopes=self.scopes + scopes)
        self._save_access_token(content, username=username)

    def _save_access_token(self, content, username):
        self.credentials = credentials_schema.load({
            'username': username,
            'access_token': content.get('access_token'),
            'refresh_token': content.get('refresh_token'),
            'org_id': None,
            'refresh_module': REFRESH_MODULE,
            'client_id': self.auth_client_id
        })
        self.save_credentials()
        
    @property
    def credentials_key(self):
        
        key = self.credentials.get('username', None)
            
        if key is None:
            key = self.credentials.get('org_id', None)
            
        return key
        
    def save_credentials(self):
        self.credentials_store.store(self.credentials)
    
    def attempt_op_with_refresh(self, op):
        try:
            return op()
        except ExpiredAccessToken:
            self.refresh_credentials()
            return op()

    def refresh_credentials(self):
        try:
            self.credentials = self._refresh_credentials_obj(self._credentials)
        except AuthUnauthorized as e:
            raise AuthException(f'Unable to refresh credentials: {str(e)} Are you logged in?')
        self.save_credentials()
        
    def logout(self):
        # Add SpintopAPI-related logout stuff
        if self.credentials and self.credentials['refresh_token']:
            self.auth_provider.revoke_refresh_token(self.credentials['refresh_token'])
            
        self.credentials_store.delete()
        self._reset_credentials()
    
    def _refresh_credentials_obj(self, credentials):
        # username and refresh_token both stay valid
        if credentials is None:
            credentials = {}
        
        username = credentials.get('username', 'unknown')

        refresh_token = credentials.get('refresh_token', None)
        
        content = self.auth_provider.refresh_access_token(refresh_token)
        
        return credentials_schema.load({
            'username': username,
            'refresh_token': refresh_token,
            'access_token': content.get('access_token'),
            'org_id': None,
            'refresh_module': REFRESH_MODULE,
            'client_id': self.auth_client_id
        })

    def credentials_match_auth_provider(self):
        return self.auth_client_id == self._credentials.get('client_id', None)
        
    def get_auth_headers(self):
        if self.credentials:
            return self.auth_provider.get_auth_headers(self.credentials.get('access_token'))
        else:
            return {}
    
    def describe(self):
        return f'Auth module initialized using {self._auth_bootstrap.describe()}'
        
    
