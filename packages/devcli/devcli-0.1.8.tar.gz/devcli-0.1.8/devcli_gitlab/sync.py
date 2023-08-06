import asyncio
import logging
from pathlib import Path

import click

from devcli_gitlab import gitlab, GitlabClient
from devcli_gitlab.git_utils import clone_or_pull_project


async def sync_tree(client: GitlabClient, group_name, install_scripts):
    projects = client.get_projects(group_name)
    await asyncio.gather(
        *[sync_repo(group_name, project, install_scripts) for project
          in
          projects])


async def sync_repo( group_name, project, install_scripts):

    relative_path = project['fullPath'].replace(f'{group_name}/', '')
    path = Path(relative_path)
    path.mkdir(parents=True, exist_ok=True)
    await clone_or_pull_project(path, project['sshUrlToRepo'])
    print('running install script')
    [install_script(path) for install_script in install_scripts]


# make pluggable
@gitlab.command()
@click.pass_obj
@click.option('--group')
@click.option('--install/--noinstall', default=False)
def sync(client: GitlabClient, group, install):
    print(install)
    install_scripts = client.ctx.get_plugin_scripts('install_script') if install else []
    logging.info(f'loaded install scripts: {install_scripts}')
    asyncio.run(sync_tree(client, group, install_scripts))
