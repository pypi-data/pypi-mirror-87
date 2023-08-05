import os
from logging import Logger
from penvy.setup.SetupStepInterface import SetupStepInterface
from penvy.shell.runner import run_shell_command


class CondaEnvironmentCreator(SetupStepInterface):
    def __init__(
        self,
        conda_executable_path: str,
        venv_dir: str,
        logger: Logger,
    ):
        self._conda_executable_path = conda_executable_path
        self._venv_dir = venv_dir
        self._logger = logger

    def get_description(self):
        return "Create the project conda environment"

    def run(self):
        self._logger.info(f"Creating Conda environment in {self._venv_dir}")

        run_shell_command(f"{self._conda_executable_path} env create -f environment.yml -p {self._venv_dir}", shell=True)

    def should_be_run(self) -> bool:
        return not os.path.isdir(self._venv_dir)
