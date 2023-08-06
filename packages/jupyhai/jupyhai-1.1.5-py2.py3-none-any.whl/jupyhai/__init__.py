# WARNING: This module may not import anything from within jupyhai
#          as it is being imported by `setup.py` – not all requirements
#          required are necessarily available during that import time.
import os

__version__ = '1.1.5'


def _jupyter_server_extension_paths():
    return [{"module": "jupyhai"}]


def _jupyter_nbextension_paths():
    import pkg_resources

    jupyhai_js = pkg_resources.resource_filename('jupyhai', 'nbextension/jupyhai.js')
    if not os.path.isfile(jupyhai_js):
        raise RuntimeError(
            '%s is not a file – was the Jupyhai package built correctly?' % jupyhai_js
        )
    return [
        {
            'section': 'notebook',
            'src': jupyhai_js,
            'dest': 'jupyhai.js',
            'require': 'jupyhai',
        },
    ]


def load_jupyter_server_extension(nb_server_app):
    from .handlers.init import prepare

    prepare(nb_server_app)
