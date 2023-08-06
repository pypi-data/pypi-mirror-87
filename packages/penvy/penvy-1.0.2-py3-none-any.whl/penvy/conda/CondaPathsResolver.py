import os
from argparse import Namespace
from penvy.parameters.ParametersResolverInterface import ParametersResolverInterface
from penvy.conda.CondaExecutablePathFinder import CondaExecutablePathFinder
from penvy.shell.runner import run_and_read_line


class CondaPathsResolver(ParametersResolverInterface):
    def __init__(
        self,
        conda_executable_path_finder: CondaExecutablePathFinder,
    ):
        self._conda_executable_path_finder = conda_executable_path_finder

    def resolve(self, config: dict, cli_args: Namespace):
        conda_executable_path = self._conda_executable_path_finder.find()
        conda_install_dir = run_and_read_line(f"{conda_executable_path} info --base", shell=True)

        return {
            "project": {
                "dir": os.getcwd(),
                "venv_dir": os.getcwd() + os.sep + ".venv",
            },
            "conda": {
                "executable_path": conda_executable_path,
                "install_dir": conda_install_dir,
                "conda_sh_path": conda_install_dir + "/etc/profile.d/conda.sh",
            },
        }
