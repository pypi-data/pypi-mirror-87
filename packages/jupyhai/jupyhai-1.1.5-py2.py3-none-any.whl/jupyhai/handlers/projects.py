from valohai_cli.api import request

from jupyhai.api_urls import PROJECTS_URL
from jupyhai.handlers.base import JupyhaiHandler
from jupyhai.utils import get_current_project


class ProjectsHandler(JupyhaiHandler):
    def get(self, tag=None):
        if tag == "current":
            project = get_current_project()
            if project:
                return self.finish(dict(project.data))  # cached JSON blob
            else:
                return self.finish({'id': None})
        else:
            response = request('get', PROJECTS_URL, params={'limit': 9999})
            projects = response.json()['results']
            return self.finish({'results': projects})
