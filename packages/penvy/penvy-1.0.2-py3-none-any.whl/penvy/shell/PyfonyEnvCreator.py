import os
from logging import Logger
from penvy.setup.SetupStepInterface import SetupStepInterface


class PyfonyEnvCreator(SetupStepInterface):
    def __init__(
        self,
        logger: Logger,
    ):
        self._logger = logger
        self._pyfony_env_script_path = os.path.expanduser("~") + os.sep + "pyfony_env.sh"

    def get_description(self):
        return "Create the pyfony_env.sh containing the ca alias to conda activate"

    def run(self):
        self._logger.info("Creating pyfony_env.sh")

        with open(self._pyfony_env_script_path, "w", encoding="utf-8") as f:
            f.write("alias ca='conda activate $PWD/.venv'")

    def should_be_run(self) -> bool:
        return not os.path.exists(self._pyfony_env_script_path)
