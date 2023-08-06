from typing import List

import click

from . import GitlabClient
from .gitlab_group import gitlab


@gitlab.command(short_help='triggers the pipeline for all projects in group')
@click.pass_obj
@click.option('--group')
@click.option('--variables', '-m', multiple=True, type=click.Tuple([str, str]),default=[])
@click.option('--include-token-under', default=None)
def trigger_pipelines(client: GitlabClient, group, variables:List, include_token_under):
    variables = [{'key':variable[0] , 'value':variable[1]} for variable in variables]
    if include_token_under:
        variables.append({'key': include_token_under, 'value': client.token})

    client.do_for_every_project(group, lambda project: project.pipelines.create({'ref': 'master', 'variables': variables}))

