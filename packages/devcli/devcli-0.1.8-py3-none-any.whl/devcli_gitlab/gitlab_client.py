import logging

import requests
from gitlab import Gitlab

from devcli import DevCliContext


class GitlabClient:

    def __init__(self, ctx: DevCliContext):
        self.token = ctx.config.get('gitlab.token')
        self.host = ctx.config.get('gitlab.host', 'https://gitlab.com')
        self.ctx = ctx
        logging.info(f'gitlab client configured with  {self.token}  and {self.host}')

        self.rest_client = Gitlab(url=self.host, private_token=self.token)
        self.graphql_headers = {"Authorization": f"Bearer {self.token}"}

    def graphql(self, query):
        request = requests.post(f'{self.host}/api/graphql', json={'query': query}, headers=self.graphql_headers)
        if request.status_code == 200:
            return request.json()
        else:
            raise Exception()

    def get_projects(self, group_path):
        query = f'''
          query {{
          group(fullPath: "{group_path}") {{
            id
            name
            projects(includeSubgroups: true) {{
              nodes {{
                id
                name
                fullPath
                sshUrlToRepo
              }}
            }}
          }}
        }}'''

        response = self.graphql(query)
        logging.info(f'response for group: {group_path}: {response}')
        return response['data']['group']['projects']['nodes']

    def do_for_every_project(self, group, func, fail_on_failure=False):

        for project in self.get_projects(group):
            gl_project = self.rest_client.projects.get(project['fullPath'], lazy=True)
            logging.info(f'processing project: {gl_project.id}')
            try:
                func(gl_project, self.ctx)
            except Exception as e:
                logging.exception(f'error during project {gl_project.id}')
