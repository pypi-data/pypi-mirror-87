import os
from logging import Logger
from penvy.setup.SetupStepInterface import SetupStepInterface


class BashProfileCreator(SetupStepInterface):
    def __init__(
        self,
        is_running_bash: bool,
        logger: Logger,
    ):
        self._is_running_bash = is_running_bash
        self._logger = logger
        self._dot_bash_profile_path = os.path.expanduser("~") + os.sep + ".bash_profile"

    def get_description(self):
        return "Create the default .bash_profile file"

    def run(self):
        self._logger.info(f"Creating default {self._dot_bash_profile_path}")

        with open(self._dot_bash_profile_path, "w", encoding="utf-8") as f:
            f.write("test -f ~/.profile && . ~/.profile\n")
            f.write("test -f ~/.bashrc && . ~/.bashrc\n")

    def should_be_run(self) -> bool:
        return self._is_running_bash and not os.path.isfile(self._dot_bash_profile_path)
