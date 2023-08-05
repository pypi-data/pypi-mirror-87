import logging
from argparse import Namespace
from penvy.parameters.ParametersResolverInterface import ParametersResolverInterface


class LoggerLevelResolver(ParametersResolverInterface):
    def resolve(self, config: dict, cli_args: Namespace):
        return {
            "logger": {"level": logging.DEBUG if cli_args.verbose is True else logging.INFO},
        }
