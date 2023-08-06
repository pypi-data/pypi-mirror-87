from datetime import timedelta

from valohai_cli.api import request

from jupyhai.api_urls import EXECUTIONS_URL
from jupyhai.consts import JUPYTER_EXECUTION_STEP_NAME
from jupyhai.excs import Problem
from jupyhai.handlers.base import JupyhaiHandler
from jupyhai.utils import get_current_project
from jupyhai.utils.auth import login_status
from jupyhai.utils.executions import get_execution_by_id


class ExecutionsHandler(JupyhaiHandler):
    def get(self, execution_id=None):
        if execution_id:
            self.finish({'results': self.get_execution_detail(execution_id)})
        else:
            self.finish({'results': self.get_executions()})

    def get_executions(self):
        if not login_status():
            raise Problem('Not logged in', code='not_logged_in')

        project = get_current_project()

        if not project:
            raise Problem('No project selected', code='no_project')

        params = {
            'project': project.id,
            'ordering': 'counter',
            'deleted': 'false',
            'limit': 1000,
            'step': JUPYTER_EXECUTION_STEP_NAME,
        }
        executions = request('get', EXECUTIONS_URL, params=params).json()[
            'results'
        ]
        for execution in executions:
            self.cleanup_execution_detail(execution)

        return executions

    def get_execution_detail(self, executionid):
        execution = get_execution_by_id(executionid)
        if not execution:
            return None

        self.cleanup_execution_detail(execution)
        return execution

    def cleanup_execution_detail(self, execution):
        execution['url'] = execution['urls']['display']
        execution['duration'] = str(
            timedelta(seconds=round(execution['duration']))
            if execution['duration']
            else ''
        ).rjust(10)
