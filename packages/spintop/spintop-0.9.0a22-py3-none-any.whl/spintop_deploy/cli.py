import click
import subprocess

@click.group()
def cli():
    pass

@cli.group()
def prefect():
    pass

@prefect.command('exec')
def exec_prefect_app():
    subprocess.Popen("exec gunicorn --bind :$PORT --workers 1 --threads 1 --timeout 0 spintop_deploy.prefect_sls:app", shell=True).wait()