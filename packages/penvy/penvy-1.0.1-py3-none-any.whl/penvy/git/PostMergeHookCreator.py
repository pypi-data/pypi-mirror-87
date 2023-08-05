import os
import platform
import subprocess
from logging import Logger
from penvy.setup.SetupStepInterface import SetupStepInterface


class PostMergeHookCreator(SetupStepInterface):
    def __init__(
        self,
        post_merge_hook_path: str,
        logger: Logger,
    ):
        self._post_merge_hook_path = post_merge_hook_path
        self._logger = logger

    def get_description(self):
        return "Create empty post-merge git hook file"

    def run(self):
        self._logger.info("Creating empty post-merge hook file")

        with open(self._post_merge_hook_path, "w", encoding="utf-8") as f:
            f.write("#!/bin/sh\n\n")

        if platform.system() != "Windows":
            subprocess.check_call(["chmod", "+x", self._post_merge_hook_path])

    def should_be_run(self) -> bool:
        return os.path.isdir(os.path.dirname(self._post_merge_hook_path)) and not os.path.isfile(self._post_merge_hook_path)
