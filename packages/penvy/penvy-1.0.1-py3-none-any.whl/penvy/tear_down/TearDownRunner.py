from logging import Logger
from typing import List
from penvy.tear_down.TearDownStepInterface import TearDownStepInterface


class TearDownRunner:
    def __init__(
        self,
        steps: List[TearDownStepInterface],
        logger: Logger,
    ):
        self._steps = steps
        self._logger = logger

    def run(self):
        for step in self._steps:
            self._logger.debug(f"Running {step.__module__}")

            step.run()
