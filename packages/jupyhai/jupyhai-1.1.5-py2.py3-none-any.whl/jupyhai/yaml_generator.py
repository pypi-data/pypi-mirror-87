import os
import shlex
import collections

import yaml
from valohai_yaml.objs import Config, Parameter, Step
from valohai_yaml.objs.environment_variable import EnvironmentVariable
from valohai_yaml.objs.input import Input

from jupyhai.consts import JUPYTER_EXECUTION_STEP_NAME
from jupyhai.utils import get_current_image, get_notebook_inputs, get_notebook_parameters, get_type_name


yaml.SafeDumper.add_representer(
    collections.OrderedDict,
    lambda dumper, data: dumper.represent_mapping('tag:yaml.org,2002:map', data.items())
)


def write_valohai_yaml(f, notebook_relative_path, content):
    notebook_dir, notebook_name = os.path.split(notebook_relative_path)

    papermill_command = " ".join(
        [
            "papermill -k python3 -f /valohai/config/parameters.yaml",
            shlex.quote("/valohai/repository/{}".format(notebook_relative_path)),
            shlex.quote("/valohai/outputs/{}".format(notebook_name)),
        ]
    )

    command = [
        "bash /valohai/repository/prepare.sh",
        papermill_command,
    ]

    jupyter_execution_step = Step(
        name=JUPYTER_EXECUTION_STEP_NAME,
        image=get_current_image(),
        command=command,
        parameters=[
            _create_parameter(attr, value)
            for (attr, value) in get_notebook_parameters(content).items()
        ],
        inputs=[
            Input(name=attr, default=value)
            for (attr, value) in get_notebook_inputs(content).items()
        ],
        environment_variables=[
            EnvironmentVariable(name="LC_ALL", default="C.UTF-8"),
            EnvironmentVariable(name="LANG", default="C.UTF-8"),
        ],
    )
    config = Config(steps=[jupyter_execution_step])
    yaml.safe_dump(config.serialize(), stream=f)


def _create_parameter(name, value):
    type_name = get_type_name(value)
    if type_name == "flag":
        return Parameter(
            name=name,
            type="flag",
            pass_true_as="-p %s True" % name,
            pass_false_as="-p %s False" % name,
            optional=True,
        )

    return Parameter(
        name=name,
        type=type_name,
        default=value,
        pass_as="-p %s {v}" % name,
        optional=True,
    )
