import sys
from typing import List
from penvy.PenvyConfig import PenvyConfig
from penvy.cli.argument_parser import create_argument_parser
from penvy.container.init import resolve_parameters, create_checks_runner, create_setup_runner, create_tear_down_runner
from penvy.poetry.DependenciesInstaller import DependenciesInstaller
from penvy.setup.SetupStepInterface import SetupStepInterface


class EnvInitRunner:
    def __init__(self, env_configs: List[PenvyConfig], container_class):
        argument_parser = self._create_argument_parser()
        self._cli_arguments = argument_parser.parse_known_args()[0]
        self._env_configs = env_configs
        self._container = container_class(self._resolve_parameters())
        self._logger = self._container.get_logger()
        self._checks_runner = self._create_checks_runner()
        self._setup_runner = self._create_setup_runner()
        self._tear_down_steps_runner = self._get_tear_down_steps_runner()

    def run(self):
        steps2run = self._setup_runner.get_steps2run()

        if self._skip_confirmation(steps2run):
            self._checks_runner.run()
        else:
            errors = self._checks_runner.check()

            if errors:
                self._checks_runner.print_errors(errors, "Fix the following errors and try again:")
                self._setup_runner.show(steps2run)
                sys.exit(1)

            self._setup_runner.show(steps2run)

            should_continue = input("\nContinue? [y/n]: ")

            if should_continue not in ["", "y", "n"]:
                self._logger.error('Press Enter, "y" or "n"')
                sys.exit(1)
            elif should_continue == "n":
                sys.exit(0)

        self._setup_runner.run()
        self._tear_down_steps_runner.run()

    def _skip_confirmation(self, steps2run: List[SetupStepInterface]):
        return self._cli_arguments.skip_confirmation or (len(steps2run) == 1 and isinstance(steps2run[0], DependenciesInstaller))

    def _create_argument_parser(self):
        return create_argument_parser()

    def _resolve_parameters(self):
        return resolve_parameters(self._env_configs, self._cli_arguments)

    def _create_checks_runner(self):
        return create_checks_runner(self._env_configs, self._container)

    def _create_setup_runner(self):
        return create_setup_runner(self._env_configs, self._container)

    def _get_tear_down_steps_runner(self):
        return create_tear_down_runner(self._env_configs, self._container)
