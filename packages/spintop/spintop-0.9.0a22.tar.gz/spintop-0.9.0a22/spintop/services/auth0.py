
import json
import jwt
import time

from functools import lru_cache
from dataclasses import dataclass

from json.decoder import JSONDecodeError
from simplejson.scanner import JSONDecodeError as SimpleJSONDecodeError

from simple_memory_cache import GLOBAL_CACHE

from ..errors import AuthUnauthorized, ExpiredAccessToken, SpintopException

from spintop.utils import spintop_session

class Auth0Error(AuthUnauthorized):
    def __init__(self, resp):
        self.content = _get_resp_content(resp)
        self.resp = resp
        super().__init__(self._create_error_message())

    def _create_error_message(self):
        desc = self.error_description
        if not desc:
            desc = str(self.content)
        return f'Request {_request_to_string(self.resp.request)!r} returned an error response: ({self.resp.status_code}) {desc}'

    @property
    def error(self):
        return self.content.get('error', None)

    @property
    def error_description(self):
        return self.content.get('error_description', None)

def _get_resp_content(resp):
    try:
        content = resp.json()
    except (JSONDecodeError, SimpleJSONDecodeError):
        content = {}
    return content

def _request_to_string(request):
    return f'{request.method} {request.url}'

class BaseAuth0Provider(object):
    def __init__(self, domain, audience, client_id, jwks_url, user_info_url, secret_key=None):
        self.domain = domain
        self.audience = audience
        self.client_id = client_id
        self.jwks_url = jwks_url
        self.user_info_url = user_info_url
        self.secret_key = secret_key

        if None in [domain, audience, client_id, jwks_url, user_info_url]:
            raise ValueError('Auth0Provider requires its parameters to not be None.')

        self.cached_jwks = GLOBAL_CACHE.MemoryCachedVar('auth_jwks')
        self.cached_jwks.on_first_access(self._retrieve_jwks)

    @property
    @lru_cache()
    def session(self):
        return spintop_session()

    def _retrieve_jwks(self):
        return self.session.get(self.jwks_url).json()
    
    def get_user_info(self, access_token):
        data = self.session.get(self.user_info_url, headers=self.get_auth_headers(access_token))
        return data.json()

    def get_auth_headers(self, access_token):
        return {'Authorization': 'Bearer ' + access_token}

    def _execute_request(self, url_path, **data):
        URL = 'https://' + self.domain  + url_path
        resp = self.session.post(URL, data = data)
        content = self._handle_errors_in_content(resp)
        return content
    
    def _handle_errors_in_content(self, resp):
        if not resp.ok:
            raise Auth0Error(resp)
    
        return _get_resp_content(resp)

    def get_jwks_key(self, access_token):
        jwks = self.cached_jwks.get()
        public_keys = {}
        for jwk in jwks['keys']:
            kid = jwk['kid']
            public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))
            
        kid = jwt.get_unverified_header(access_token)['kid']
        key = public_keys[kid]
        return key

    def jwt_verify(self, access_token):
        try:
            payload = self.decode(access_token)
        except jwt.ExpiredSignatureError:
            raise ExpiredAccessToken("Token Expired")
        except jwt.PyJWTError:
            # invalidate jwks cache and try ONCE more.
            self.cached_jwks.invalidate()
            payload = self.decode(access_token)
        return payload
    
    def decode(self, access_token):
        key = self.get_jwks_key(access_token)
        return jwt.decode(access_token, key=key, algorithms=['RS256'], audience=[self.client_id, self.audience])

class Auth0Provider(BaseAuth0Provider):
    def client_credentials(self):
        if not self.secret_key:
            raise SpintopException('Client credentials grant requires a secret key.')

        return self._execute_request('/oauth/token',
            grant_type = 'client_credentials',
            client_id = self.client_id,
            client_secret = self.secret_key,
            audience = self.audience,
        )

    def authenticate(self, username, password, scopes=[]):
        return self._execute_request('/oauth/token',
            grant_type = 'password',
            username = username,
            password = password,
            audience = self.audience,
            client_id = self.client_id,
            scope = ' '.join(scopes)
        )

    def DeviceAuthorizationFlow(self):
        return DeviceAuthorizationFlow(self)

    def request_device_code(self, scopes=[]):
        return self._execute_request('/oauth/device/code',
            audience = self.audience,
            client_id = self.client_id,
            scope = ' '.join(scopes)
        )

    def check_device_code_approval(self, device_code):
        return self._execute_request('/oauth/token',
            grant_type = 'urn:ietf:params:oauth:grant-type:device_code',
            device_code = device_code,
            client_id = self.client_id
        )
    
    def refresh_access_token(self, refresh_token):
        if not refresh_token:
            raise AuthUnauthorized('No refresh token exists; unable to execute operation.')

        return self._execute_request('/oauth/token',
            grant_type = 'refresh_token',
            client_id = self.client_id,
            refresh_token = refresh_token
        )

    def revoke_refresh_token(self, refresh_token):
        self._execute_request('/oauth/revoke',
            client_id = self.client_id,
            token = refresh_token
        )
    

class DeviceAuthorizationFlow(object):
    def __init__(self, auth0_provider):
        self.auth0 = auth0_provider
        self.device_code_response = None

    def request_verification_url(self, scopes=[]):
        raw_response = self.auth0.request_device_code(scopes=scopes)
        self.device_code_response = DeviceCodeResponse(**raw_response)
        return self.device_code_response

    def wait_for_approval(self):
        interval = self.device_code_response.interval
        expires_in = self.device_code_response.expires_in
        device_code = self.device_code_response.device_code

        start = time.time()

        response = None

        while time.time() - start < expires_in:
            try:
                response = self.auth0.check_device_code_approval(device_code)
                break
            except Auth0Error as e:
                if e.error == "expired_token":
                    raise AuthUnauthorized("Did not receive an access token in time.")
                elif e.error == "access_denied":
                    raise AuthUnauthorized("User did not accept access.")
                elif e.error == "slow_down":
                    interval = interval + 2
                else:
                    # authorization_pending
                    pass
                    
                time.sleep(interval)
        
        if not response:
            raise AuthUnauthorized("No access token received.")
            
        return response
    
@dataclass
class DeviceCodeResponse():
    device_code: str
    user_code: str
    verification_uri: str
    verification_uri_complete: str
    expires_in: int
    interval: int
