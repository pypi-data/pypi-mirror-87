from logging import Logger
from penvy.setup.SetupStepInterface import SetupStepInterface
from penvy.shell.runner import run_shell_command


class DependenciesInstaller(SetupStepInterface):
    def __init__(
        self,
        poetry_executable_path: str,
        logger: Logger,
    ):
        self._poetry_executable_path = poetry_executable_path
        self._logger = logger

    def get_description(self):
        return "Install all python dependencies"

    def run(self):
        self._logger.info("Installing dependencies from poetry.lock")

        run_shell_command(f"{self._poetry_executable_path} install --no-root", shell=True)

    def should_be_run(self) -> bool:
        return True
