import sys
from logging import Logger
from penvy.check.CheckInterface import CheckInterface
from penvy.shell.detector import detect_shell, ShellVarNotSetException, WIN_CMD, ZSH, BASH, GIT_BASH


class ShellCheck(CheckInterface):
    def __init__(
        self,
        logger: Logger,
    ):
        self._logger = logger

    def run(self):
        try:
            shell_name = detect_shell()
        except ShellVarNotSetException:
            self._logger.warning("Unable to resolve shell type from the SHELL env variable")
            return

        if shell_name == WIN_CMD and sys.argv[0][-8:] != "/init.py":
            return "Cannot run under cmd.exe, please use Git Bash instead"

        if shell_name not in [ZSH, BASH, GIT_BASH]:
            self._logger.warning(f"Your shell {shell_name} is not fully supported, use bash or zsh instead")
            return

        self._logger.debug(f"Shell {shell_name} ok")
