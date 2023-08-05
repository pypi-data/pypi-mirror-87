import os
import platform
from penvy.cmd.detector import is_windows_cmd
from penvy.shell.name_extractor import extract_shell_name

WIN_CMD = "win_cmd"
GIT_BASH = "git_bash"
BASH = "bash"
ZSH = "zsh"


class ShellVarNotSetException(Exception):
    pass


def detect_shell():
    if is_windows_cmd():
        return WIN_CMD

    if platform.system() == "Windows":
        return GIT_BASH

    if "ZSH_VERSION" in os.environ:
        return ZSH

    if "BASH_VERSION" in os.environ:
        return BASH

    if "SHELL" not in os.environ:
        raise ShellVarNotSetException()

    return extract_shell_name(os.environ["SHELL"])
