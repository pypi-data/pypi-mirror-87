import filecmp
import os
import platform
import subprocess
from shutil import copyfile
from logging import Logger
from penvy.setup.SetupStepInterface import SetupStepInterface
from penvy.libroot import get_libroot


class CondaScriptsCreator(SetupStepInterface):
    def __init__(
        self,
        venv_dir: str,
        logger: Logger,
    ):
        self._venv_dir = venv_dir
        self._activate_script_source_path = f"{get_libroot()}/conda/activate.d/env_vars.sh"
        self._activate_script_target_path = f"{venv_dir}/etc/conda/activate.d/env_vars.sh"
        self._deactivate_script_source_path = f"{get_libroot()}/conda/deactivate.d/env_vars.sh"
        self._deactivate_script_target_path = f"{venv_dir}/etc/conda/deactivate.d/env_vars.sh"
        self._logger = logger

    def get_description(self):
        return "Create/update conda environment activation and deactivation scripts"

    def run(self):
        self._logger.info("Setting up Conda activation & deactivation scripts")

        self._logger.info("Seting-up conda/activate.d")
        self._copy_script(self._activate_script_source_path, self._activate_script_target_path)

        self._logger.info("Seting-up conda/deactivate.d")
        self._copy_script(self._deactivate_script_source_path, self._deactivate_script_target_path)

    def _copy_script(self, script_source_path: str, script_target_path: str):
        os.makedirs(os.path.dirname(script_target_path), exist_ok=True)

        copyfile(script_source_path, script_target_path)

        if platform.system() != "Windows":
            subprocess.check_call(["chmod", "+x", script_target_path])

    def should_be_run(self) -> bool:
        return (
            not os.path.exists(self._activate_script_target_path)
            or not os.path.exists(self._deactivate_script_target_path)
            or not filecmp.cmp(self._activate_script_source_path, self._activate_script_target_path)
            or not filecmp.cmp(self._deactivate_script_source_path, self._deactivate_script_target_path)
        )
