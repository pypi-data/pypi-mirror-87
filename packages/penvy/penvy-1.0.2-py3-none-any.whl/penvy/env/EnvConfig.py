from abc import ABC
from typing import List
from penvy.parameters.ParametersResolverInterface import ParametersResolverInterface
from penvy.container.dicontainer import Container


class EnvConfig(ABC):
    def get_parameters(self) -> dict:
        return {}

    def get_parameters_resolvers(self, default_config: dict) -> List[ParametersResolverInterface]:
        return []

    def get_checks(self, container: Container):
        return []

    def get_setup_steps(self, container: Container):
        return []

    def get_tear_down_steps(self, container: Container):
        return []
