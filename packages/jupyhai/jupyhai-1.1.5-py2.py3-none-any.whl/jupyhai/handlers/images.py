from jupyhai.handlers.base import JupyhaiHandler
from jupyhai.utils import get_current_image


class ImagesHandler(JupyhaiHandler):
    def get(self, tag=None):
        if tag == "current":
            self.finish({"image": get_current_image()})
        else:
            # TODO: Implement
            self.finish({'image': ''})
