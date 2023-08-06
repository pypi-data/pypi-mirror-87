from logging import Logger
from penvy.tear_down.TearDownStepInterface import TearDownStepInterface


class ActivateCondaEnvCall(TearDownStepInterface):
    def __init__(
        self,
        venv_dir: str,
        logger: Logger,
    ):
        self._venv_dir = venv_dir
        self._logger = logger

    def run(self):
        venv_path_forward_slashes = self._venv_dir.replace("\\", "/")

        self._logger.info("Setup completed. Active Conda environment now:")
        self._logger.info(f"conda activate {venv_path_forward_slashes}")
