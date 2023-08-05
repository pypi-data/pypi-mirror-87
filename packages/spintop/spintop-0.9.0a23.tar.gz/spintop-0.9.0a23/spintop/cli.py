import os
import sys
import click
import traceback
import logging
import threading
import time
from pprint import pformat, pprint
from tabulate import tabulate

from . import logs, storage
from .auth import AuthModule
from .compat import format_exception
from .errors import SpintopException
from .models import Query
from .env import Spintop


class CLIParseException(SpintopException):
    pass

logger = logs._logger('cli')

_spintop = None 
spintop_kwargs = {}
def spintop():
    global _spintop, spintop_kwargs
    if _spintop is None:
        _spintop = Spintop(**spintop_kwargs)
    return _spintop

@click.group()
@click.option('-v', '--verbose', is_flag=True, default=False)
@click.option('--url', default=None)
@click.option('--org-id', default=None)
def _cli(verbose, url, org_id):
    global spintop_kwargs
    logs.VERBOSE = verbose
    spintop_kwargs.update(dict(verbose=verbose, api_url=url, org_id=org_id))

@_cli.command('site-data-dir')
def site_data_dir():
    click.echo(storage.SITE_DATA_DIR)
    
@_cli.command('login')
def login():
    spintop().login() # Check first before prompting

@_cli.command('login-cli')
@click.option('--username', default=None)
@click.option('--password', default=None)
def login_cli_command(username, password):
    if username is None and password is not None:
        raise CLIParseException('You cannot specify the password as option but not the username')
    
    spintop().assert_no_login() # Check first before prompting
    
    if username is None:
        username = click.prompt('Username')
        
    if password is None:
        password = click.prompt('Password', hide_input=True)
    
    spintop().login_user_pass(username, password)

@_cli.command('logout')
def logout_command():
    stored_username = spintop().stored_logged_username()
    if stored_username:
        if click.confirm('Logging out %s. Continue ?' % stored_username):
            spintop().logout()
    else:
        click.echo('No credentials stored.')

@_cli.command('userinfo')
def get_orgs():
    user_info = spintop().user_info
    click.echo(user_info)

@_cli.command('orginfo')
@click.argument('org_key')
def get_orgs(org_key):
    org_info = spintop().get_org_info(org_key)
    click.echo(org_info)

@_cli.command('ls-orgs')
def get_orgs():
    orgs = spintop().get_user_orgs()
    click.echo(orgs)

@_cli.command('ls-tests')
def list_tests():
    tests = spintop().tests.retrieve()
    tests = list(tests)
    for test in tests:
        click.echo(test.data.test_id)

@_cli.command('test-api-private')
def test_private_command():
    print(spintop().test_private_endpoint().json())
    
@_cli.command('force-corrupt-access-token')
def force_corrupt_access_token():
    spintop_api = spintop()
    spintop_api.auth.credentials.access_token = spintop_api.auth.credentials.access_token[0:-4]
    spintop_api.auth.save_credentials()


def cli(args=None, internal=True):
    try:
        return _cli(args, prog_name='spintop')
    except Exception as e:
        if logs.VERBOSE:
            click.echo(traceback.format_exc())
        else:
            click.echo(format_exception(e))
    except SystemExit:
        if not internal:
            raise

def main():
    cli(internal=False)

if __name__ == '__main__':
    main()