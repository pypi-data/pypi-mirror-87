from valohai_cli.api import request

from jupyhai.api_urls import EXECUTIONS_URL
from jupyhai.handlers.base import JupyhaiHandler


class StopHandler(JupyhaiHandler):
    def post(self, execution_id=None):
        if execution_id:
            self.finish({'path': self.stop_execution(execution_id)})
            return
        self.log.error("Error stopping execution: No execution ID.")

    def stop_execution(self, id):
        return request('post', '%s%s/stop/' % (EXECUTIONS_URL, id)).json()
