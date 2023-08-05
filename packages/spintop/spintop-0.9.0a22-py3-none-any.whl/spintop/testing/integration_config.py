
import yaml


class IntegrationConfig(object):
    def __init__(self, username, password, expected_org):
        self.username = username
        self.password = password
        self.expected_org = expected_org
        self.spintop_api_url = None
        
    def login_and_assert(self, auth_module):
        self.login(auth_module)
        self.assert_credentials_good(auth_module.credentials)
        self.assert_org_in_users(auth_module)

    def assert_credentials_good(self, credentials):
        assert credentials['username'] == self.username

    def assert_credentials_empty(self, credentials):
        assert not credentials

    def login(self, auth_module):
        auth_module.login_user_pass(self.username, self.password)

    def assert_org_in_users(self, auth_module):
        assert self.expected_org in auth_module.user_orgs

    def assert_org_match(self, org):
        assert org['key'] == self.expected_org

    @classmethod
    def load_file(cls, filepath):
        with open(filepath) as conffile:
            return cls(**yaml.load(conffile, Loader=yaml.FullLoader))
        