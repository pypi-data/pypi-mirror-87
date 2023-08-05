import re
from distutils.version import StrictVersion
from logging import Logger
from penvy.check.CheckInterface import CheckInterface
from penvy.shell.runner import run_and_read_line


class CondaVersionCheck(CheckInterface):
    def __init__(
        self,
        minimal_version: str,
        conda_executable_path: str,
        logger: Logger,
    ):
        self._minimal_version = minimal_version
        self._conda_executable_path = conda_executable_path
        self._logger = logger

    def run(self):
        self._logger.debug(f"Using conda executable: {self._conda_executable_path}")

        first_line = run_and_read_line(f"{self._conda_executable_path} --version", shell=True)

        conda_version = re.sub(r"^conda ([\d.]+).*$", "\\1", first_line)

        if StrictVersion(conda_version) < StrictVersion(self._minimal_version):
            return f"Conda version {conda_version} is too old, please update to {self._minimal_version} or higher"

        self._logger.debug(f"Conda version {conda_version} ok")
