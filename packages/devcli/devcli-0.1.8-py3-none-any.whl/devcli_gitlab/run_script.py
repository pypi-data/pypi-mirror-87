import importlib

import click
import gitlab

from devcli_gitlab import GitlabClient


@gitlab.command()
@click.option('--group')
@click.option('--name')
@click.option('--script', type=click.Path(exists=True))
def run_script(client: GitlabClient, group, name, script):
    spec = importlib.util.spec_from_file_location("script", script)
    script = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(script)
    client.do_for_every_project(group, script.run)

