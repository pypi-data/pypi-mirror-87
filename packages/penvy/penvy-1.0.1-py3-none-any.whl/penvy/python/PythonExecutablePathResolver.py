import os
from argparse import Namespace

from penvy.parameters.ParametersResolverInterface import ParametersResolverInterface


class PythonExecutablePathResolver(ParametersResolverInterface):
    def resolve(self, config: dict, cli_args: Namespace):
        venv_dir = config["project"]["venv_dir"]

        if os.name == "nt":
            python_executable_path = venv_dir + "\\python.exe"
        else:
            python_executable_path = venv_dir + "/bin/python"

        return {
            "python": {
                "executable_path": python_executable_path,
            }
        }
