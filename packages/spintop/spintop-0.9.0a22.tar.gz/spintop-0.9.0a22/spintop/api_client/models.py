import re
from typing import List, Union, Any, Dict

from spintop.models import BaseDataClass, get_serializer, FilterSpec

class DimensionSpec(BaseDataClass):
    name: str
    field_type: str
    label: str = None
    description: str = None

class TableSpec(BaseDataClass):
    filters: List[FilterSpec] = list
    custom_dimensions: List[DimensionSpec] = list

class EnvDataspecs(BaseDataClass):
    steps: TableSpec = None
    production_nodes: TableSpec = None
    external_project_id: str = None
    external_dataset_id: str = None
    # readonly:
    project_id: str = None
    dataset_id: str = None

class OrgDataEnv(BaseDataClass):
    name: str
    vars: dict = dict
    dataspecs: EnvDataspecs = None

class Dashboard(BaseDataClass):
    name: str
    base_url: str = None
    sharing_secret: str = None
    sharing_token: str = None
    url: str = None

class Organization(BaseDataClass):
    key: str
    project_id: str
    default_env: str = None
    dashboards: List[Dashboard] = list
    envs: List[OrgDataEnv] = list

    def __post_init__(self):
        super().__post_init__()
        validate_tenant_key(self.key)

    def find_env(self, env_name):
        for env in self.envs:
            if env.name == env_name:
                return env
        else:
            raise ValueError(f'Org {self.key} has no env named {env_name}')

    def env_dataset_name(self, env_name):
        return f'data__{sanitize_tenant_key(self.key)}__{env_name}'

ALLOWED = re.compile(r'[^a-z0-9-_]')
def validate_tenant_key(tenant_key):
    valid = not bool(ALLOWED.match(tenant_key))
    if not valid:
        raise InvalidOrgKey(tenant_key)

def sanitize_tenant_key(tenant_key):
    validate_tenant_key(tenant_key)
    return tenant_key.replace('-', '_')

class ManyOrganizations(BaseDataClass):
    orgs: List[Organization]

    def __iter__(self):
        return iter(self.orgs)
    
    def find_org(self, org_key):
        for org in self.orgs:
            if org.key == org_key:
                return org
        else:
            raise ValueError(f'No org named {org_key}')
    

class User(BaseDataClass):
    username: str = None
    user_id: str
    scope: List[str]
    permissions: List[str]
    user_type: str
    organizations: List[Organization]

class UnitMatch(BaseDataClass):
    lc_type: str
    match: str