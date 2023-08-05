import os
import json
import base64
import platform

from flask import Blueprint, request

import prefect
from prefect import Flow

from .agent import ServerlessAgent

class SpintopServerlessPrefectContext(object):
    def __init__(self, prefect_project, storage, agent_name='sls', id_map_encoded=None, param_provider=None):
        if param_provider:
            load_secrets(param_provider)

        self.prefect_project = prefect_project
        self.storage = storage
        self.agent_name = agent_name
        self.id_map = {}
        self._flows = {}

        if id_map_encoded:
            self.decode_id_map(id_map_encoded)

    def add_flow(self, *flows):
        for flow in flows:
            flow.storage = self.storage
            self.storage.add_flow(flow)
            self._flows[flow.name] = flow
        return flow

    def build(self):
        self.storage.build()

    def register(self):
        self.build()
        for flow_name, flow in self._flows.items():
            flow_id = flow.register(project_name=self.prefect_project, build=False)
            self.id_map[flow_name] = flow_id
        return self.id_map
    
    def encode_id_map(self):
        json_data = json.dumps(self.id_map)
        base64_bytes = base64.b64encode(json_data.encode('utf-8'))
        return base64_bytes.decode('ascii')

    def decode_id_map(self, map_encoded):
        base64_bytes = map_encoded.encode('ascii')
        json_data = base64.b64decode(base64_bytes).decode('utf-8')
        self.id_map = json.loads(json_data)
        return self.id_map

    def run(self, flow_name, parameters={}, **kwargs):
        flow_id = self.id_map.get(flow_name, None)
        if flow_id is None:
            raise ValueError(f'No flow with name {flow_name}')
        
        ephemeral_agent = ServerlessAgent(name=self.agent_name, labels=[flow_id], show_flow_logs=True)
        ephemeral_agent.run_flow_id(flow_id, labels=[flow_id], parameters=parameters)

    def flask_blueprint(self):
        from flask import Blueprint, request

        blueprint = Blueprint('prefect_flows', __name__)
        
        links = {}
        for flow_name, flow_id in self.id_map.items():
            blueprint.route(f'/{flow_name}', methods=['POST', 'GET'])(
                self.create_route(flow_name, flow_id)
            )
            links[flow_name] = flow_id


        @blueprint.route('/', methods=['GET'])
        def index():
            return {
                'status': 'OK',
                'flows': links
            }

        return blueprint

    def create_route(self, flow_name, flow_id):
        def _route():
            try:
                parameters = request.json
            except Exception as e:
                parameters = {}

            ephemeral_agent = ServerlessAgent(name=self.agent_name, labels=[flow_id], show_flow_logs=True)
            ephemeral_agent.run_flow_id(flow_id, labels=[flow_id], parameters=parameters)
            return 'OK', 200
        
        _route.__name__ = flow_name
        return _route

def load_secrets(param_provider):
    os.environ['PREFECT__CLOUD__AGENT__AUTH_TOKEN'] = param_provider.get_environ_or_param_value('PREFECT__CLOUD__AGENT__AUTH_TOKEN', default='')
    prefect.context.config.cloud.agent.auth_token = os.environ["PREFECT__CLOUD__AGENT__AUTH_TOKEN"]
    prefect.config.cloud.agent.auth_token = os.environ["PREFECT__CLOUD__AGENT__AUTH_TOKEN"]

    os.environ['PREFECT__CLOUD__AUTH_TOKEN'] = param_provider.get_environ_or_param_value('PREFECT__CLOUD__AUTH_TOKEN', default='')
    prefect.context.config.cloud.auth_token = os.environ["PREFECT__CLOUD__AUTH_TOKEN"]
    prefect.config.cloud.auth_token = os.environ["PREFECT__CLOUD__AUTH_TOKEN"]