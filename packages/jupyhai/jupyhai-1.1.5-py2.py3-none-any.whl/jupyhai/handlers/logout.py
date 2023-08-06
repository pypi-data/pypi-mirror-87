from jupyhai.handlers.base import JupyhaiHandler
from jupyhai.utils.auth import login_status, logout


class LogoutHandler(JupyhaiHandler):
    def get(self):
        self.finish({'result': login_status()})

    def post(self):
        self.log.info("Logging out...")
        logout()
        success = not login_status()
        if success:
            self.log.info("Logged out.")
        self.finish({'success': success})
