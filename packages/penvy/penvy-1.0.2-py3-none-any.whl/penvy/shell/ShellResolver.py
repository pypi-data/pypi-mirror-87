from argparse import Namespace
from typing import Optional
from penvy.parameters.ParametersResolverInterface import ParametersResolverInterface
from penvy.shell.detector import detect_shell, ShellVarNotSetException, BASH, GIT_BASH, ZSH


class ShellResolver(ParametersResolverInterface):
    def resolve(self, config: dict, cli_args: Namespace):
        try:
            shell = detect_shell()
        except ShellVarNotSetException:
            return self._return(None, False, False)

        is_bash = shell in [BASH, GIT_BASH]
        is_zsh = shell == ZSH

        return self._return(shell, is_bash, is_zsh)

    def _return(self, name: Optional[str], is_bash: bool, is_zsh: bool):
        return {
            "shell": {
                "name": name,
                "is_bash": is_bash,
                "is_zsh": is_zsh,
            },
        }
