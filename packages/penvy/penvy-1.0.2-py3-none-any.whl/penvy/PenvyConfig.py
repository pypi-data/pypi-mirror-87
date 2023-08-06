from typing import List
from penvy.env.EnvConfig import EnvConfig
from penvy.conda.CondaExecutablePathFinder import CondaExecutablePathFinder
from penvy.conda.CondaPathsResolver import CondaPathsResolver
from penvy.logger.LoggerLevelResolver import LoggerLevelResolver
from penvy.parameters.ParametersResolverInterface import ParametersResolverInterface
from penvy.container.dicontainer import Container
from penvy.poetry.PoetryPathResolver import PoetryPathResolver
from penvy.python.PythonExecutablePathResolver import PythonExecutablePathResolver
from penvy.shell.ShellResolver import ShellResolver


class PenvyConfig(EnvConfig):
    def get_parameters(self) -> dict:
        return {
            "logger": {"name": "env-init"},
            "conda": {"minimal_version": "4.7.12"},
            "git": {"minimal_version": "2.24.0"},
            "poetry": {"install_version": "1.0.0"},
        }

    def get_parameters_resolvers(self, default_config: dict) -> List[ParametersResolverInterface]:
        return [
            ShellResolver(),
            LoggerLevelResolver(),
            CondaPathsResolver(CondaExecutablePathFinder()),
            PythonExecutablePathResolver(),
            PoetryPathResolver(),
        ]

    def get_checks(self, container: Container):
        return [
            container.get_shell_check(),
            container.get_pyproject_checker(),
            container.get_conda_version_check(),
            container.get_git_version_check(),
        ]

    def get_setup_steps(self, container: Container):
        return [
            container.get_conda_environment_creator(),
            container.get_conda_scripts_creator(),
            container.get_bash_profile_creator(),
            container.get_pyfony_env_creator(),
            container.get_file_creator_bashrc(),
            container.get_source_conda_appender_bashrc(),
            container.get_source_pyfony_env_appender_bashrc(),
            container.get_file_creator_zshrc(),
            container.get_source_conda_appender_zshrc(),
            container.get_source_pyfony_env_appender_zshrc(),
            container.get_poetry_installer(),
            container.get_dot_env_creator(),
            container.get_dependencies_installer(),
            container.get_post_merge_hook_creator(),
            container.get_dependencies_install_hook_creator(),
        ]

    def get_tear_down_steps(self, container: Container):
        return [container.get_activate_conda_env_call()]
