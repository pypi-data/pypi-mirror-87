import re
from distutils.version import StrictVersion
from logging import Logger
from penvy.check.CheckInterface import CheckInterface
from penvy.shell.runner import run_and_read_line


class GitVersionCheck(CheckInterface):
    def __init__(
        self,
        minimal_version: str,
        logger: Logger,
    ):
        self._minimal_version = minimal_version
        self._logger = logger

    def run(self):
        first_line = run_and_read_line("git --version", shell=True)

        git_version = re.sub(r"^git version ([0-9.]+)[.].+$", "\\1", first_line)

        if StrictVersion(git_version) < StrictVersion(self._minimal_version):
            return f"Git version {git_version} is too old, please update to {self._minimal_version} or higher"

        self._logger.debug(f"Git version {git_version} ok")
