import os
from logging import Logger
from penvy.setup.SetupStepInterface import SetupStepInterface
from penvy.shell.home_path_shortener import shorten_home_path


class RcFileCreator(SetupStepInterface):
    def __init__(
        self,
        rc_file_path: str,
        expected_shell_is_running: callable,
        logger: Logger,
    ):
        self._rc_file_path = rc_file_path
        self._rc_file_path_shorten = shorten_home_path(rc_file_path)
        self._expected_shell_is_running = expected_shell_is_running
        self._logger = logger

    def get_description(self):
        return f"Create {self._rc_file_path_shorten}"

    def run(self):
        self._logger.info(f"Creating {self._rc_file_path_shorten}")

        open(self._rc_file_path, "a").close()

    def should_be_run(self) -> bool:
        return self._expected_shell_is_running and not os.path.isfile(self._rc_file_path)
