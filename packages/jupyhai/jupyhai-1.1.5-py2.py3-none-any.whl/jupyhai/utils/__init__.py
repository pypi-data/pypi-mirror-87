import json
import os

from notebook.notebookapp import list_running_servers
from valohai_cli.ctx import get_project
from valohai_cli.settings import settings

from jupyhai import consts
from jupyhai.consts import DEFAULT_IGNORE, DEFAULT_IMAGE, DEFAULT_TITLE


def parse_ipynb(content):
    """
    "Smartly" parse content that contains a notebook.

    * If a string, it's first JSON deserialized.
    * If it's a "wrapped" dict (i.e. contains "type" == "notebook" and "content"), unwraps the content
    * Asserts the content smells like a notebook ("nbformat")

    :param content: See above.
    :return: Notebook data.
    """
    if isinstance(content, str):
        content = json.loads(content)
    if not isinstance(content, dict):
        raise ValueError('Ipynb not a dict')
    if content.get('type') == 'notebook':
        content = content['content']

    nbformat = content.get('nbformat')
    if not isinstance(nbformat, int):
        raise ValueError('Nbformat value %s invalid' % nbformat)
    return content


def get_notebook_parameters(content):
    code = get_notebook_tagged_code(content, "parameters")
    return execute_cell_code(code, "parameters")


def get_notebook_inputs(content):
    code = get_notebook_tagged_code(content, "inputs")
    return execute_cell_code(code, "inputs")


def get_notebook_tagged_code(content, tag):
    obj = parse_ipynb(content)
    result = ""
    for cell in obj['cells']:
        if (
            cell
            and 'source' in cell
            and 'metadata' in cell
            and 'tags' in cell['metadata']
            and tag in cell['metadata']['tags']
        ):
            result += '%s\r\n' % ''.join(cell['source'])
    return result


def get_type_name(value):
    pythonic_name = type(value).__name__
    if pythonic_name == 'int':
        return "integer"
    if pythonic_name == 'bool':
        return "flag"
    if pythonic_name == 'str':
        return "string"
    return pythonic_name


def execute_cell_code(code, tag):
    ns = {}
    try:
        compiled = compile(code, "<CODE>", "exec")
    except SyntaxError as err:
        raise SyntaxError(f"Syntax error in notebook cell tagged \"{tag}\" at line {err.lineno}: {err}.") from err
    try:
        exec(compiled, globals(), ns)
    except Exception as err:
        raise Exception(f"Error executing notebook cell tagged \"{tag}\": {err}") from err
    return ns


def filter_environments(environments):
    return [env for env in environments if env['enabled']]


def get_current_project():
    return get_project(consts.ROOT_DIRECTORY)


def get_current_image():
    return settings.persistence.get('jupyhai_image', DEFAULT_IMAGE)


def get_current_environment():
    return settings.persistence.get('jupyhai_environment')


def get_current_title():
    return settings.persistence.get('jupyhai_title', DEFAULT_TITLE)


def get_current_ignore():
    return settings.persistence.get('jupyhai_ignore', DEFAULT_IGNORE)


def get_current_host_is_minihai():
    return settings.persistence.get('jupyhai_host_is_minihai', False)


def get_notebook_server():
    return next(list_running_servers())
