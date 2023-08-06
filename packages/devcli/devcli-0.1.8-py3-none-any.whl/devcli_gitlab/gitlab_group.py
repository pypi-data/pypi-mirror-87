import click
from devcli import cli
from devcli_gitlab.gitlab_client import GitlabClient


@cli.group()
@click.pass_context
def gitlab(ctx):
    ctx.obj = GitlabClient(ctx.obj)
