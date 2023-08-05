import os

import requests 
import platform
import functools

from contextlib import contextmanager
from pprint import pformat
from uuid import uuid4

from functools import partial
from ..errors import SpintopException

from ..auth import AuthModule
from ..logs import _logger
from ..compat import VERSION
from ..storage import TEMP_DIR

from .persistence_facade import SpintopAPIPersistenceFacade
from .analytics import SpintopAPIAnalytics
from .models import ManyOrganizations

from spintop import __version__
from spintop.utils.requests_utils import spintop_session

logger = _logger('spintop-api')

TEMPORARY_DOWNLOAD_FOLDER = os.path.join(TEMP_DIR, '.spintop-api-download-cache')
if not os.path.exists(TEMPORARY_DOWNLOAD_FOLDER):
    try:
        os.makedirs(TEMPORARY_DOWNLOAD_FOLDER)
    except:
        logger.warning(f'Unable to makedirs({TEMPORARY_DOWNLOAD_FOLDER}) even though file does not exist.')
    
class SpintopClientError(SpintopException):
    pass

class SpintopAPIError(SpintopException):
    def __init__(self, resp):
        try:
            json = resp.json()
        except Exception:
            json = {}
        
        error_type = json.get('error_type', 'UNKNOWN')
        error_messages = json.get('error_messages', {})
        messages_as_string = '\n\t'.join(['%s: %s' % (key, value) for key, value in error_messages.items()])
        
        if not messages_as_string:
            messages_as_string = json.get('error_message') # singular, the direct exception message
            
        message = f'Request {resp.request.method} {resp.url} A {resp.status_code} error of type "{error_type}" occured while contacting API.\n\t{messages_as_string}'
        
        super().__init__(message)

        self.error_type = error_type
        self.resp = resp

def refresh_if_fail_gen(auth_module):
    try:
        yield
    except SpintopAPIError as e:
        if e.resp.status_code == 401 and e.error_type in ('auth_token_verification_failed',) :
            # Attempt ONCE to refresh the credentials and retry.
            auth_module.refresh_credentials()
            yield
        else:
            raise

def SpintopAPISession(prefix, auth_module):
    if prefix is None:                                                                                                                                                                                                                                                                                                                             
        prefix = ""                                                                                                                                                                                                                                                                                                                                
    else:                                                                                                                                                                                                                                                                                                                                          
        prefix = prefix.rstrip('/')                                                                                                                                                                                                                                                                                                      

    def attempt_request(f, method, url, *args, **kwargs):
        if 'headers' not in kwargs: kwargs['headers'] = {}
        kwargs['headers'].update(auth_module.get_auth_headers())
        resp = f(method, prefix + url, *args, **kwargs)
        if not resp.ok:
            raise SpintopAPIError(resp)
        return resp
    
    def new_request(prefix, *args, **kwargs):
        
        try:
            resp = attempt_request(*args, **kwargs)
        except SpintopAPIError as e:
            if e.resp.status_code == 401 and e.error_type in ('auth_token_verification_failed', 'auth_missing_header') :
                # Attempt ONCE to refresh the credentials and retry.
                auth_module.refresh_credentials()
                resp = attempt_request(*args, **kwargs)
            else:
                raise
        return resp
    
    s = spintop_session()
    s.request = partial(new_request, prefix, s.request)
    return s

class SpintopAPIClientModule(object):
    def __init__(self, api_url, org_id=None, auth=None, message_publisher=None):
        self._session = None

        self.auth = auth
        
        self._org_id = org_id
        self._messages_publisher = message_publisher
        self._persistence_facade = None
        self._analytics = None
        
        self._api_url = api_url
        self._user_info = None
        self._api_spec = None
        self._default_org = None
        self._machine = None

    @property
    def api_url(self):
        if callable(self._api_url):
            return self._api_url()
        else:
            return self._api_url

    @api_url.setter
    def api_url(self, value):
        self._session = None
        self._api_url = value

    @property
    def session(self):
        if not self._session:
            self._session = self.new_session()
        return self._session

    @property
    def user_info(self):
        if self._user_info is None:
            self._user_info = self.session.get(self.get_link('tenancy.user_info')).json()
        return self._user_info

    @property
    def api_spec(self):
        if self._api_spec is None:
            # Use a new session here, since we need api_spec to init auth during session retrival.
            self._api_spec = self.new_session().get('/api/').json()
        return self._api_spec
    
    def invalidate_api_spec(self):
        self._api_spec = None

    @property
    def selected_org_id(self):
        if self._org_id is None:
            raise ValueError('No org selected')
        
        return self._org_id

    @property
    def records(self):
        return self._persistence_facade

    @property
    def local_messages(self):
        return self._messages_publisher

    @property
    def analytics(self):
        return self._analytics

    @property
    def api_spintop_version(self):
        return self.api_spec['versions']['spintop']

    def register_persistence_facade(self, persistence_facade):
        self._persistence_facade = persistence_facade

    def register_analytics(self, analytics):
        self._analytics = analytics

    def login(self):
        """Interactive login"""
        self.auth.assert_no_login() # Check first before prompting

        with self.login_browser() as device_flow_response:
            logger.info(f'User code is {device_flow_response.user_code!r}')
            logger.info(f'If this device is headless (without a browser), you may visit this link to authorize this device on another machine: {device_flow_response.verification_uri_complete}')

    def login_user_pass(self, username, password):
        self.auth.login_user_pass(username, password)

    def login_browser(self):
        return self.auth.login_device_flow()

    def stored_logged_username(self):
        if self.auth.credentials:
            return self.auth.credentials.get('username')
        else:
            return None
    
    def logout(self):
        return self.auth.logout()
    
    def get_user_orgs(self):
        return self.auth.user_orgs

    def new_session(self):
        return SpintopAPISession(self.api_url, self.auth)
    
    def reset_session(self):
        self._session = None

    def test_private_endpoint(self):
        resp = self.session.get(self.get_link('core.private'))
        return resp

    def get_org_info(self, org_id=None):
        return self.session.get(self.get_link('tenancy.org_info', org_id=org_id)).json()

    def create_org(self, org_id, data):
        return self.session.post(self.get_link('tenancy.create_org', org_id=org_id), json=data).json()

    def update_org(self, org_id, data):
        return self.create_org(org_id, data)

    def list_orgs(self):
        data = self.session.get(self.get_link('tenancy.list_orgs')).json()
        return ManyOrganizations.from_dict(data)

    def list_dashboards(self, org_id):
        return self.session.get(self.get_link('ui.dashboards', org_id=org_id)).json()

    def create_secret_token(self, org_id, sharing_token):
        return self.session.post(self.get_link('ui.secret_token', org_id=org_id, sharing_token=sharing_token)).json()['token']

    def get_topics(self, org_id=None):
        return self.session.get(self.get_link('backend.topics', org_id=org_id)).json()

    def get_records_env(self, org_id=None):
        """ An env that points to the API itself """
        return self.session.get(self.get_link('records.env', org_id=org_id)).json()

    def update_spintop_metadata(self, metadata, org_id=None):
        return self.session.put(self.get_link('backend.spintop_metadata', org_id=org_id), json=metadata).json()

    def _call_session(self, method, link_name_or_parts, link_params={}, **kwargs):
        fn = getattr(self.session, method)

        if not isinstance(link_name_or_parts, str):
            link_name = '.'.join(link_name_or_parts)
        else:
            link_name = link_name_or_parts

        uri = self.get_link(link_name, **link_params)
        return fn(uri, **kwargs)

    def execute_query(self, query_name, env_name=None, params={}):
        query_params = {}
        if env_name:
            query_params['env_name'] = env_name
        return self.session.put(
            self.get_link('analytics.execute_query', query_name=query_name), 
            params=query_params,
            json=params
        ).json()

    def get_records_env_direct_database_context(self, org_id=None):
        """ An env that points to the API's underlying database (with the API's URI)"""
        if org_id is None: org_id = self.selected_org_id
        env = self.get_records_env(org_id)
        org_info = self.get_org_info(org_id)
        return env.new_database_context(org_info['database_name'])

    def _compare_api_version(self):
        ours = __version__
        apis = self.api_spintop_version
        return f'API version: {apis!r}, ours: {ours!r}'

    def get_link(self, link_name, org_id=None, **kwargs):
        links = self.api_spec['_links']
        try:
            base_link = links[link_name]
        except KeyError:
            # Link does not exist. Check API version.
            raise KeyError(f'No link named {link_name!r} @ {self.api_url}. {self._compare_api_version()}. Availabe link names: {set(links.keys())}')

        if '<org_id>' in base_link:
            if org_id is None:
                org_id = self.selected_org_id

            kwargs['org_id'] = org_id

        link = base_link
        for key, value in kwargs.items():
            link = link.replace(f'<{key}>', value)

        if '<' in link or '>' in link:
            raise SpintopClientError(f'Link {base_link!r} is missing placeholder values. Received {kwargs.keys()!r}')

        return link

    def api(self):
        return _APIDiscovery(self)
        
class _APIDiscovery(object):
    def __init__(self, spintop, link_parts=[]):
        self.spintop = spintop
        self.link_parts = link_parts

    def __getattr__(self, link_part):
        return self.__class__(self.spintop, self.link_parts + [link_part])

    def __call(self, method, link_params={}, **kwargs):
        return self.spintop._call_session(method, self.link_parts, link_params=link_params, **kwargs)

    def get(self, *args, **kwargs):
        return self.__call('get', *args, **kwargs)

    def post(self, *args, **kwargs):
        return self.__call('post', *args, **kwargs)

    def put(self, *args, **kwargs):
        return self.__call('put', *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.__call('delete', *args, **kwargs)