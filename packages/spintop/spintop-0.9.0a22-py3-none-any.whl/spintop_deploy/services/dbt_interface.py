import os
import sys
import yaml
import tempfile
from pprint import pprint
import subprocess

import dbt.main

from spintop.api_client.models import ManyOrganizations

class BigqueryOutputFactory(object):
    def __init__(self, project_id, keyfile=None, threads=40, impersonate_service_account=None):
        if keyfile is None:
            keyfile = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', None)

        if keyfile:
            keyfile = os.path.abspath(keyfile)
            method = 'service-account'
        else:
            method = 'oauth'
        
        self.keyfile = keyfile
        self.project_id = project_id
        self.method = method
        self.threads = threads
        self.impersonate_service_account = impersonate_service_account

    @classmethod
    def from_env(cls, env):
        kwargs = dict(
            project_id=env.GOOGLE_CLOUD_PROJECT
        )

        keyfile = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', None)

        if not keyfile: 
            if env.IMPERSONATE_SERVICE_ACCOUNT:
                kwargs['impersonate_service_account'] = env.IMPERSONATE_SERVICE_ACCOUNT
        else:
            kwargs['keyfile'] = keyfile
        
        return cls(**kwargs)

    def create(self, org_data, env_name):
        dataset = org_data.env_dataset_name(env_name)
        return dict(
            type='bigquery',
            method=self.method,
            threads=self.threads,
            keyfile=self.keyfile,
            project=self.project_id,
            impersonate_service_account=self.impersonate_service_account,
            dataset=dataset
        )

class SpintopOrgProfileFactory(object):
    def __init__(self, output_factory):
        self.output_factory = output_factory

    def create_profile(self, org_data):
        org_key = org_data.key
        return {
            org_key: dict(
                outputs={
                    env.name: self.output_factory.create(org_data, env.name) for env in org_data.envs
                }
            )
        }

def create_all_profiles(all_profiles):
    profiles = {}
    for p in all_profiles:
        profiles.update(p)
    return profiles

def dbt_run(project_dir, profile_dir, org_key, env_data, dbt_args=[], debug=False):
    vars_string = yaml.safe_dump(env_data.vars, default_flow_style=True).strip()
    print(f'Running DBT in project-dir={project_dir} with target={env_data.name}. Vars are:')
    print(vars_string)
    args = [
        'run',
        '--project-dir', project_dir,
        '--profiles-dir', profile_dir,
        '--profile', org_key,
        '--target', env_data.name,
        '--vars', vars_string
    ] + list(dbt_args)

    if debug:
        args.insert(0, '-d')
    
    # print('Would run')
    # pprint(args)
    p = subprocess.Popen([sys.executable, '-m', __name__] + args)
    out, err = p.communicate()

    if p.returncode != 0:
        raise RuntimeError('Error while executing dbt run.')


class DBTInterface(object):
    def __init__(self, project_dir, output_factory, temp_dir=None):
        self.project_dir = project_dir
        self.output_factory = output_factory

        if temp_dir is None:
            temp_dir = tempfile.mkdtemp(suffix='dbt-interface')

        self.temp_dir = temp_dir
        self.orgs = None

    @property
    def profiles_file(self):
        return os.path.join(self.temp_dir, 'profiles.yml')

    def load_orgs(self, orgs):
        self.orgs = ManyOrganizations(orgs=list(orgs))
        factory = SpintopOrgProfileFactory(self.output_factory)
        all_profiles = [factory.create_profile(org) for org in orgs]

        profiles = create_all_profiles(all_profiles)
        with open(self.profiles_file, 'w+') as profiles_file:
            yaml.safe_dump(profiles, profiles_file)

    def run(self, org_key, env_name, dbt_args=[], debug=False):
        env = self.orgs.find_org(org_key).find_env(env_name)
        return dbt_run(
            project_dir=self.project_dir, 
            profile_dir=self.temp_dir,
            org_key=org_key, 
            env_data=env, 
            dbt_args=dbt_args, 
            debug=debug
        )

if __name__ == '__main__':
    print('CWD: ' + os.getcwd())
    dbt.main.main()

    

