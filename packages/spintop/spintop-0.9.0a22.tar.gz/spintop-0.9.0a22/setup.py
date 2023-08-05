import os
import sys
from glob import glob

from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, 'spintop', 'VERSION')) as version_file:
    VERSION = version_file.read().strip()
packages = find_packages()

setup(
    name='spintop',
    version=VERSION,
    description='The python client to spintop.io',
    author='William Laroche',
    author_email='william.laroche@tackv.ca',
    maintainer='William Laroche',
    maintainer_email='william.laroche@tackv.ca',
    packages=packages,
    package_data={
        'spintop': ['VERSION']
    },
    install_requires=[
        'anytree',
        'appdirs',
        'click',
        'cryptography',
        'dataclasses>=0.6',
        'gitpython',
        'jinja2',
        'marshmallow>=3.5',
        'marshmallow-dataclass',
        'marshmallow-union',
        'marshmallow-jsonschema',
        'pkginfo',
        'PyJWT',
        'psutil',
        'pytz',
        'pyyaml',
        'python-dateutil',
        'requests',
        'tabulate',
        'tblib',
        'incremental-module-loader',
        'simplejson',
        'simple-memory-cache',
        'xmltodict'
    ],
    extras_require={
        'postgres': [
            'sqlalchemy',
            'psycopg2'
        ],
        'bigquery': [
            'jsonschema>=2.6.0',
            'singer-python>=1.5.0',
            'google-api-python-client>=1.6.2',
            'google-cloud>=0.34.0',
            'google-cloud-bigquery>=1.9.0',
            'oauth2client'
        ],
        'deploy': [
            'flask',
            'prefect',
            'google-cloud-secret-manager',
            'google-cloud-storage',
            'google-cloud-pubsub',
            'google-cloud-tasks'
        ]
    },
    setup_requires=[
        'wheel>=0.29.0,<1.0',
    ],
    tests_require=[
        'mock>=2.0.0',
        'pytest>=2.9.2',
        'pytest-cov>=2.2.1',
    ],
)