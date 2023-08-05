import atexit
import os
import warnings
import dotenv
from datetime import datetime

import pytz
import pytest
import pytest_dependency # pylint: disable=unused-import

from .integration_config import IntegrationConfig

from spintop import Spintop
from spintop.env import SpintopEnv

from spintop.auth import AuthModule, InMemoryCredentialsStore
from spintop.api_client import SpintopAPIClientModule, SpintopAPISpecAuthBootstrap

from spintop.generators.random_gen import RandomTestGenerator
from spintop.models import SpintopTestRecordCollection

dotenv.load_dotenv()

def _integration_file(config):
    return os.path.join(config.rootdir, 'integration_secrets.yml')

@pytest.fixture(scope="session")
def random_generator():
    return RandomTestGenerator()

@pytest.fixture(scope="session")
def auth_module(integration_config):
    return AuthModule(
        auth_bootstrap=SpintopAPISpecAuthBootstrap(integration_config.spintop_api_url) if integration_config else None,
        credentials_store=InMemoryCredentialsStore()
    )

@pytest.fixture(scope="session")
def spintop_env(integration_config):
    if integration_config:
        assert 'SPINTOP_M2M_CLIENT_ID' in os.environ
        assert 'SPINTOP_M2M_SECRET_KEY' in os.environ
        return SpintopEnv( 
            api_url=integration_config.spintop_api_url, 
            org_id=integration_config.expected_org
        )
    else:
        return SpintopEnv()

@pytest.fixture(scope="session", autouse=True)
def spintop_api_module(integration_config, spintop_env):
    if not integration_config:
        return None
    else:
        return spintop_env.spintop_factory()

@pytest.fixture(scope="session", autouse=True)
def spintop_user_api_module(integration_config, auth_module, spintop_env):
    if not integration_config:
        return None
    else:
        return spintop_env.spintop_factory(auth_factory=lambda: auth_module)

@pytest.fixture(scope="module")
def raw_collection(random_generator):
    raw_collection = SpintopTestRecordCollection(
        random_generator.generate(
            count=2, 
            start_datetime=datetime(year=2020, month=1, day=1, tzinfo=pytz.utc), 
            test_phases=('phase1', 'phase2'),
            measures=('measure1', 'measure2'),
            failure_rate=1.0
        )
    )
    return raw_collection

@pytest.fixture(scope="module")
def flat_record_collection(raw_collection):
    return raw_collection

@pytest.fixture()
def flat_test_record(flat_record_collection):
    return flat_record_collection.records[0]

KNOWN_HOSTS = {
    'dev': 'https://dev.cloud.spintop.io',
    'prod': 'https://cloud.spintop.io',
    None: 'http://127.0.0.1:5079'
}

def pytest_addoption(parser):
    parser.addoption(
        "--test-against", action="store", default=None, help=f"The spintop API url to test against, or one of {set(KNOWN_HOSTS.keys())}"
    )

def pytest_configure(config):
    config.addinivalue_line("markers", "integration: mark test as auth/api integration test")

def pytest_collection_modifyitems(config, items):
    integration_file = _integration_file(config)
    if os.path.exists(integration_file):
        return
    else:
        warnings.warn(f'Integration file {integration_file!r} does not exist; integration with API will not be tested. This file should be located in the pytest rootdir.')
        skip_slow = pytest.mark.skip(reason="need --integration-file option to run")
        for item in items:
            if "integration" in item.keywords:
                item.add_marker(skip_slow)

def pytest_runtest_makereport(item, call):
    if "incremental" in item.keywords:
        if call.excinfo is not None:
            parent = item.parent
            parent._previousfailed = item

def pytest_runtest_setup(item):
    previousfailed = getattr(item.parent, "_previousfailed", None)
    if previousfailed is not None:
        pytest.xfail("previous test failed (%s)" % previousfailed.name)

@pytest.fixture(scope="session")
def integration_config(request):
    filepath = _integration_file(request.config)
    if os.path.exists(filepath):
        config = IntegrationConfig.load_file(filepath)
        host = request.config.getoption("--test-against")
        host = KNOWN_HOSTS.get(host, host)
        config.spintop_api_url = host
        create_atexit_print_test_against(host)
    else:
        config = None
    return config

def create_atexit_print_test_against(spintop_api_url):
    def report():
        print(f"Tested against {spintop_api_url!r}")
    atexit.register(report)

@pytest.fixture()
def spintop():
    return Spintop()

@pytest.fixture()
def flat_test_record(flat_record_collection):
    return flat_record_collection.records[0]