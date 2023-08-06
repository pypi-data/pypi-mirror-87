import os
from logging import Logger
from penvy.setup.SetupStepInterface import SetupStepInterface
from penvy.shell.home_path_shortener import shorten_home_path
from penvy.string.string_in_file import file_contains_string


class SourcePyfonyEnvAppender(SetupStepInterface):
    def __init__(
        self,
        rc_file_path: str,
        expected_shell_is_running: callable,
        logger: Logger,
    ):
        self._rc_file_path = rc_file_path
        self._rc_file_path_shorten = shorten_home_path(rc_file_path)
        self._pyfony_env_script_path = os.path.expanduser("~") + os.sep + "pyfony_env.sh"
        self._pyfony_env_script_path_shoten = shorten_home_path(self._pyfony_env_script_path)
        self._expected_shell_is_running = expected_shell_is_running
        self._logger = logger

    def get_description(self):
        return f'Add "source {self._pyfony_env_script_path_shoten}" into {self._rc_file_path_shorten}'

    def run(self):
        self._logger.info(f'Adding "source {self._pyfony_env_script_path_shoten}" to {self._rc_file_path_shorten}')

        with open(self._rc_file_path, "a") as f:
            f.write(f"source {self._pyfony_env_script_path_shoten}\n")

    def should_be_run(self) -> bool:
        return self._expected_shell_is_running and (
            not os.path.isfile(self._rc_file_path)
            or not file_contains_string(f"source {self._pyfony_env_script_path_shoten}", self._rc_file_path)
        )
