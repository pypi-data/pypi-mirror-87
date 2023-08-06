from argparse import Namespace
from typing import List
from penvy.parameters.ParametersMerger import ParametersMerger
from penvy.parameters.ParametersResolverInterface import ParametersResolverInterface


class ResolvedParametersBuilder:
    def __init__(self, resolvers: List[ParametersResolverInterface]):
        self._resolvers = resolvers
        self._config_merger = ParametersMerger()

    def build(self, cli_args: Namespace):
        config = dict()

        for resolver in self._resolvers:
            new_config = resolver.resolve(config, cli_args)

            self._config_merger.merge(config, new_config)

        return config
