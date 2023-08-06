from penvy.container.diservice import diservice


class Container:
    def __init__(
        self,
        parameters: dict,
    ):
        self.services = {}
        self._parameters = parameters

    @property
    def parameters(self):
        return self._parameters

    @diservice
    def get_logger(self):
        from penvy.logger.logger_factory import get_logger

        return get_logger(
            self._parameters["logger"]["name"],
            self._parameters["logger"]["level"],
        )

    @diservice
    def get_poetry_installer(self):
        from penvy.poetry.PoetryInstaller import PoetryInstaller

        return PoetryInstaller(
            self._parameters["python"]["executable_path"],
            self._parameters["poetry"]["executable_path"],
            self._parameters["poetry"]["install_version"],
            self.get_logger(),
        )

    @diservice
    def get_conda_environment_creator(self):
        from penvy.conda.CondaEnvironmentCreator import CondaEnvironmentCreator

        return CondaEnvironmentCreator(
            self._parameters["conda"]["executable_path"], self._parameters["project"]["venv_dir"], self.get_logger()
        )

    @diservice
    def get_conda_scripts_creator(self):
        from penvy.conda.CondaScriptsCreator import CondaScriptsCreator

        return CondaScriptsCreator(self._parameters["project"]["venv_dir"], self.get_logger())

    @diservice
    def get_bash_profile_creator(self):
        from penvy.bash.BashProfileCreator import BashProfileCreator

        return BashProfileCreator(
            self._parameters["shell"]["is_bash"],
            self.get_logger(),
        )

    @diservice
    def get_file_creator_bashrc(self):
        import os
        from penvy.shell.RcFileCreator import RcFileCreator

        return RcFileCreator(os.path.expanduser("~") + os.sep + ".bashrc", self._parameters["shell"]["is_bash"], self.get_logger())

    @diservice
    def get_file_creator_zshrc(self):
        import os
        from penvy.shell.RcFileCreator import RcFileCreator

        return RcFileCreator(os.path.expanduser("~") + os.sep + ".zshrc", self._parameters["shell"]["is_zsh"], self.get_logger())

    @diservice
    def get_source_conda_appender_bashrc(self):
        import os
        from penvy.conda.SourceCondaAppender import SourceCondaAppender

        return SourceCondaAppender(
            os.path.expanduser("~") + os.sep + ".bashrc",
            self._parameters["conda"]["conda_sh_path"],
            self._parameters["shell"]["is_bash"],
            self.get_logger(),
        )

    @diservice
    def get_source_conda_appender_zshrc(self):
        import os
        from penvy.conda.SourceCondaAppender import SourceCondaAppender

        return SourceCondaAppender(
            os.path.expanduser("~") + os.sep + ".zshrc",
            self._parameters["conda"]["conda_sh_path"],
            self._parameters["shell"]["is_zsh"],
            self.get_logger(),
        )

    @diservice
    def get_source_pyfony_env_appender_bashrc(self):
        import os
        from penvy.shell.SourcePyfonyEnvAppender import SourcePyfonyEnvAppender

        return SourcePyfonyEnvAppender(
            os.path.expanduser("~") + os.sep + ".bashrc", self._parameters["shell"]["is_bash"], self.get_logger()
        )

    @diservice
    def get_source_pyfony_env_appender_zshrc(self):
        import os
        from penvy.shell.SourcePyfonyEnvAppender import SourcePyfonyEnvAppender

        return SourcePyfonyEnvAppender(os.path.expanduser("~") + os.sep + ".zshrc", self._parameters["shell"]["is_zsh"], self.get_logger())

    @diservice
    def get_pyfony_env_creator(self):
        from penvy.shell.PyfonyEnvCreator import PyfonyEnvCreator

        return PyfonyEnvCreator(self.get_logger())

    @diservice
    def get_dot_env_creator(self):
        from penvy.dotenv.DotEnvCreator import DotEnvCreator

        return DotEnvCreator(self._parameters["project"]["dir"], self.get_logger())

    @diservice
    def get_dependencies_installer(self):
        from penvy.poetry.DependenciesInstaller import DependenciesInstaller

        return DependenciesInstaller(self._parameters["poetry"]["executable_path"], self.get_logger())

    @diservice
    def get_activate_conda_env_call(self):
        from penvy.conda.ActivateCondaEnvCall import ActivateCondaEnvCall

        return ActivateCondaEnvCall(self._parameters["project"]["venv_dir"], self.get_logger())

    @diservice
    def get_shell_check(self):
        from penvy.shell.ShellCheck import ShellCheck

        return ShellCheck(self.get_logger())

    @diservice
    def get_pyproject_checker(self):
        from penvy.poetry.PyprojectChecker import PyprojectChecker

        return PyprojectChecker(self.get_logger())

    @diservice
    def get_conda_version_check(self):
        from penvy.conda.CondaVersionCheck import CondaVersionCheck

        return CondaVersionCheck(
            self._parameters["conda"]["minimal_version"],
            self._parameters["conda"]["executable_path"],
            self.get_logger(),
        )

    @diservice
    def get_git_version_check(self):
        from penvy.git.GitVersionCheck import GitVersionCheck

        return GitVersionCheck(
            self._parameters["git"]["minimal_version"],
            self.get_logger(),
        )

    @diservice
    def get_post_merge_hook_creator(self):
        from penvy.git.PostMergeHookCreator import PostMergeHookCreator

        return PostMergeHookCreator(self._parameters["project"]["dir"] + "/.git/hooks/post-merge", self.get_logger())

    @diservice
    def get_dependencies_install_hook_creator(self):
        from penvy.poetry.DependenciesInstallHookCreator import DependenciesInstallHookCreator

        return DependenciesInstallHookCreator(
            self._parameters["project"]["dir"] + "/.git/hooks/post-merge",
            self._parameters["poetry"]["executable_path"],
            self.get_logger(),
        )
