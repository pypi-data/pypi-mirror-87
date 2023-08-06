from argparse import Namespace
from typing import List
from penvy.env.EnvConfig import EnvConfig
from penvy.check.CheckInterface import CheckInterface
from penvy.parameters.ParametersMerger import ParametersMerger
from penvy.parameters.ParametersResolverInterface import ParametersResolverInterface
from penvy.parameters.ResolvedParametersBuilder import ResolvedParametersBuilder
from penvy.container.dicontainer import Container
from penvy.setup.SetupRunner import SetupRunner
from penvy.setup.SetupStepInterface import SetupStepInterface
from penvy.check.ChecksRunner import ChecksRunner
from penvy.tear_down.TearDownRunner import TearDownRunner
from penvy.tear_down.TearDownStepInterface import TearDownStepInterface


def create_checks_runner(env_configs: List[EnvConfig], container: Container):
    checks: List[CheckInterface] = []

    for env_config in env_configs:
        checks = checks + env_config.get_checks(container)

    return ChecksRunner(checks, container.get_logger())


def create_setup_runner(env_configs: List[EnvConfig], container: Container):
    setup_steps: List[SetupStepInterface] = []

    for env_config in env_configs:
        setup_steps = setup_steps + env_config.get_setup_steps(container)

    return SetupRunner(setup_steps, container.get_logger())


def create_tear_down_runner(env_configs: List[EnvConfig], container: Container):
    tear_down_steps: List[TearDownStepInterface] = []

    for env_config in env_configs:
        tear_down_steps = tear_down_steps + env_config.get_tear_down_steps(container)

    return TearDownRunner(tear_down_steps, container.get_logger())


def resolve_parameters(env_configs: List[EnvConfig], cli_args: Namespace):
    parameters_merger = ParametersMerger()

    parameters = {}
    config_resolvers: List[ParametersResolverInterface] = []

    for env_config in env_configs:
        parameters = parameters_merger.merge(parameters, env_config.get_parameters())

    for env_config in env_configs:
        config_resolvers = config_resolvers + env_config.get_parameters_resolvers(parameters)

    resolved_parameters_builder = ResolvedParametersBuilder(config_resolvers)
    resolved_parameters = resolved_parameters_builder.build(cli_args)

    return parameters_merger.merge(parameters, resolved_parameters)
