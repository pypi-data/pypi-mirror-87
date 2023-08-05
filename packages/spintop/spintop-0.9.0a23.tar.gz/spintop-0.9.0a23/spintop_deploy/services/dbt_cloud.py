import requests

class DbtCloudInterface(object):
    def __init__(self, env):
        self.env = env
        self.token = env.DBT_CLOUD_AUTH_TOKEN
    
    def trigger_job(self, job_url, cause='Triggered from Spintop Data Analysis.', use_git_sha=True, use_git_branch=None):
        api_token = self.env.DBT_CLOUD_AUTH_TOKEN
        if not api_token:
            raise RuntimeError('DBT trigger requires DBT_CLOUD_AUTH_TOKEN in env.')

        body = {'cause': cause}
        if use_git_branch:
            body['git_branch'] = use_git_branch
        elif self.env.COMMIT_SHA and use_git_sha:
            body['git_sha'] = self.env.COMMIT_SHA

        r = requests.post(job_url, json=body, headers={'Authorization': f'Bearer {api_token}'})
        r.raise_for_status()