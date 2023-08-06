import click
from gitlab import GitlabGetError

from . import GitlabClient
from .gitlab_group import gitlab


@gitlab.command()
@click.option('--group')
@click.option('--name')
@click.argument('file', type=click.File('r'))
@click.pass_obj
def add_file(client: GitlabClient, group, name, file):
    contents = file.read()
    client.do_for_every_project(group, add_file_function(name, contents))


def add_file_function(file_name, file_contents):
    def add_file_to_project(project):

        try:
            f = project.files.create({'file_path': file_name,
                                      'branch': 'master',
                                      'content': file_contents,
                                      # 'author_email': 'job.denoo@dearhealth.com',
                                      # 'author_name': 'Job de Noo',
                                      'commit_message': 'added pytest'})

        except GitlabGetError as e:
            print(e)
            if e.response_code == 404:
                print('contunueing')
                pass
            else:
                raise e
    return add_file_to_project
