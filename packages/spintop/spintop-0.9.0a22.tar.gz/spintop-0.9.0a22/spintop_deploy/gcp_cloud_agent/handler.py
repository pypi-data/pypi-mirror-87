import os
import time
import platform

from pprint import pprint


from flask import Flask, request
from spintop import __version__
from spintop.logs import setup_logging
from spintop.api_client import SpintopAPIError

from spintop_deploy.logs import _logger
from spintop_deploy.env import SpintopDeployEnv

from .bigquery_audit_handler import bigquery_audit_handler

logger = _logger('cloud-agent')

def create_app(init_env=None):

    app = Flask(__name__)
    bootstrap_env = SpintopDeployEnv(init_env)
    modules = bootstrap_env.deployment_provider_modules()
    modules.load(setup_logging)

    param_provider = modules['param_provider']

    if not bootstrap_env.SPINTOP_M2M_SECRET_KEY:
        bootstrap_env.SPINTOP_M2M_SECRET_KEY  = param_provider.get_environ_or_param_value('SPINTOP_M2M_SECRET_KEY')

    spintop_client = bootstrap_env.spintop_factory()
    modules.update(spintop_client=spintop_client)

    logger.info(spintop_client.auth.describe())

    @app.route('/', methods=['GET'])
    def index():
        
        status = None
        remote_status = None
        authentication_ok = True
        authorization_ok = True
        try:
            org_info = spintop_client.get_org_info()
        except SpintopAPIError as e:
            status = 'ERROR'
            remote_status = 'OK'

            org_info = e.resp.json()
            if e.resp.status_code == 401:
                authentication_ok = False
                authorization_ok = False
            elif e.resp.status_code == 403:
                authorization_ok = False

        except Exception as e:
            status = 'ERROR'
            remote_status = 'ERROR'

            org_info = 'Unable to retrieve org info: ' + str(e)
        
        return {
            'status': 'OK' if status is None else status,
            'version': __version__,
            'org_info': org_info,
            'remote': spintop_client.api_url,
            'remote_status': 'OK' if remote_status is None else remote_status,
            'remote_authentication': 'OK' if authentication_ok else 'ERROR',
            'remote_authorization': 'OK' if authorization_ok else 'ERROR'
        }, 200 if status is None else 500 # Config error

    handler = modules.load(bigquery_audit_handler)

    @app.route('/', methods=['POST'])
    def notification():
        try:
            data = request.json
            print('POST content:')
            print(data)
        except Exception as e:
            print('Unable to get JSON: ' + str(e))
            raise

        handled = handler(data)
        
        return { 'handled': handled }, 200
    
    return app