import json

from valohai_cli.api import request

from jupyhai.api_urls import EXECUTIONS_URL
from jupyhai.consts import JUPYTER_EXECUTION_STEP_NAME
from jupyhai.handlers.base import JupyhaiHandler
from jupyhai.utils import (
    get_current_environment,
    get_current_image,
    get_current_project,
    get_notebook_inputs,
    get_notebook_parameters,
    get_current_title)


class ExecuteHandler(JupyhaiHandler):
    def initialize(self, root_dir):
        self.root_dir = root_dir

    def post(self):
        args = self.get_json_body()

        commit = args['commit']
        content = json.dumps(args['content'])
        environment_id = get_current_environment()
        image = get_current_image()
        project_id = get_current_project().id
        title = get_current_title()

        try:
            execution_obj = self.execute(
                commit=commit,
                content=content,
                environment_id=environment_id,
                image=image,
                project_id=project_id,
                title=title,
            )
        except Exception as err:
            self.log.error(err, exc_info=True)
            raise

        self.finish({'success': True, 'execution': execution_obj})

    def execute(
        self,
        commit,
        content,
        project_id,
        environment_id,
        image,
        title="Notebook execution",
    ):
        payload = {
            'commit': commit,
            'project': project_id,
            'inputs': get_notebook_inputs(content) or {},
            'parameters': get_notebook_parameters(content) or {},
            'environment_variables': {
                'LC_ALL': 'C.UTF-8',
                'LANG': 'C.UTF-8',
            },
            'step': JUPYTER_EXECUTION_STEP_NAME,
            'image': image,
            'title': title,
        }

        if environment_id:
            payload['environment'] = environment_id

        return request('post', EXECUTIONS_URL, json=payload).json()
