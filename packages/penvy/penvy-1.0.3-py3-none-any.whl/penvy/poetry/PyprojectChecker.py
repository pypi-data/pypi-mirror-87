import os
from logging import Logger
from penvy.check.CheckInterface import CheckInterface


class PyprojectChecker(CheckInterface):
    def __init__(
        self,
        logger: Logger,
    ):
        self._logger = logger
        self._pyproject_file_path = os.getcwd() + os.sep + "pyproject.toml"

    def run(self):
        if not os.path.isfile(self._pyproject_file_path):
            return "pyproject.toml file required by Poetry is missing in the current folder"

        self._logger.debug("pyproject.toml ok")
