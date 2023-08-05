from abc import ABC, abstractmethod
from argparse import Namespace


class ParametersResolverInterface(ABC):
    @abstractmethod
    def resolve(self, config: dict, cli_args: Namespace):
        pass
