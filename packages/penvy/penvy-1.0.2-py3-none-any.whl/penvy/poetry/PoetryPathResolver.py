import os
from argparse import Namespace
from penvy.parameters.ParametersResolverInterface import ParametersResolverInterface


class PoetryPathResolver(ParametersResolverInterface):
    def resolve(self, config: dict, cli_args: Namespace):
        return {
            "poetry": {
                "executable_path": os.path.expanduser("~") + "/.poetry/bin/poetry",
            },
        }
