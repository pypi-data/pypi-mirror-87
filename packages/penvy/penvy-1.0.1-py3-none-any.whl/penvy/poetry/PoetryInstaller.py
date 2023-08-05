import os
import shutil
import urllib.request
import tempfile
from logging import Logger
from penvy.setup.SetupStepInterface import SetupStepInterface
from penvy.shell.runner import run_shell_command
from penvy.string.random_string_generator import generate_random_string


class PoetryInstaller(SetupStepInterface):
    def __init__(
        self,
        python_executable_path: str,
        poetry_executable_path: str,
        install_version: str,
        logger: Logger,
    ):
        self._python_executable_path = python_executable_path
        self._poetry_executable_path = poetry_executable_path
        self._install_version = install_version
        self._logger = logger

    def get_description(self):
        return f"Install poetry {self._install_version}"

    def run(self):
        self._logger.info("Installing Poetry globally")

        tmp_dir = tempfile.gettempdir()
        target_file_name = tmp_dir + f"/get-poetry_{generate_random_string(5)}.py"

        url = "https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py"
        urllib.request.urlretrieve(url, target_file_name)

        run_shell_command(f"{self._python_executable_path} {target_file_name} -y --version {self._install_version}", shell=True)

    def should_be_run(self) -> bool:
        return not self._poetry_on_path() and not os.path.isfile(self._poetry_executable_path)

    def _poetry_on_path(self):
        poetry_executable_path = shutil.which("poetry")

        return (
            poetry_executable_path is not None
            and poetry_executable_path[0:5] != "/mnt/"  # WSL2: poetry executable being reused from Windows
        )
