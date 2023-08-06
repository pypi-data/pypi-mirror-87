from jupyhai.handlers.base import JupyhaiHandler
from valohai_cli.commands.execution.outputs import get_execution_outputs


class OutputsHandler(JupyhaiHandler):
    def get(self, execution_id):
        self.finish({'results': get_execution_outputs({'id': execution_id})})
