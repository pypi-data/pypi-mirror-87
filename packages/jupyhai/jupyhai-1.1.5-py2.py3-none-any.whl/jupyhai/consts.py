# WARNING: This module may not import anything from within jupyhai
#          as it is being imported by `setup.py` – not all requirements
#          required are necessarily available during that import time.
import os

HOST = os.environ.get("VALOHAI_HOST", "https://app.valohai.com")
ROOT_DIRECTORY = os.getcwd()
NOTEBOOK_INSTANCE_ID = os.environ.get("VALOHAI_NOTEBOOK_INSTANCE_ID")
PROJECT_ID = os.environ.get("VALOHAI_PROJECT_ID")
DEFAULT_IMAGE = "valohai/pypermill"
DEFAULT_TITLE = "Notebook execution"
PAPERMILL_VERSION = "8445fb0d984af248d6946b6672b3e42633f21e51"
DEFAULT_IGNORE = ["*.ipynb"]
JUPYTER_VERSION = "1.0.0"
SEABORN_VERSION = "0.9.0"
NBCONVERT_VERSION = "5.5.0"
JUPYTER_EXECUTION_STEP_NAME = "jupyter_execution"

# These patterns are always prepended to any user ignore patterns.
ALWAYS_IGNORE = [pat for pat in os.environ.get('ALWAYS_IGNORE', '').split(',') if pat]
