import os
import shutil
from logging import Logger
from penvy.setup.SetupStepInterface import SetupStepInterface


class DotEnvCreator(SetupStepInterface):
    def __init__(
        self,
        project_dir: str,
        logger: Logger,
    ):
        self._logger = logger
        self._dot_env_path = project_dir + os.sep + ".env"
        self._dot_env_dist_path = project_dir + os.sep + ".env.dist"

    def get_description(self):
        return "Create .env file from the .env.dist template"

    def run(self):
        self._logger.info("Creating .env file from the .env.dist template")

        shutil.copy(self._dot_env_dist_path, self._dot_env_path)

    def should_be_run(self) -> bool:
        return os.path.isfile(self._dot_env_dist_path) and not os.path.isfile(self._dot_env_path)
