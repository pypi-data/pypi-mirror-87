import os
from logging import Logger
from penvy.setup.SetupStepInterface import SetupStepInterface
from penvy.shell.home_path_shortener import shorten_home_path
from penvy.string.string_in_file import file_contains_string


class SourceCondaAppender(SetupStepInterface):
    def __init__(
        self,
        rc_file_path,
        conda_sh_path: str,
        expected_shell_is_running: callable,
        logger: Logger,
    ):
        self._rc_file_path = rc_file_path
        self._rc_file_path_shorten = shorten_home_path(rc_file_path)
        self._conda_sh_path = conda_sh_path
        self._conda_sh_path_shorten = shorten_home_path(conda_sh_path)
        self._expected_shell_is_running = expected_shell_is_running
        self._logger = logger

    def get_description(self):
        return f'Add "source {self._conda_sh_path_shorten}" into {self._rc_file_path_shorten}'

    def run(self):
        conda_sh_path_foward_slashes = self._conda_sh_path_shorten.replace("\\", "")

        self._logger.info(f"Adding {conda_sh_path_foward_slashes} to {self._rc_file_path_shorten}")

        with open(self._rc_file_path, "a") as f:
            f.write(f"source {conda_sh_path_foward_slashes}\n")

    def should_be_run(self) -> bool:
        return self._expected_shell_is_running and (
            not os.path.isfile(self._rc_file_path) or not file_contains_string("/etc/profile.d/conda.sh", self._rc_file_path)
        )
