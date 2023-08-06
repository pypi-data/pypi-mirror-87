import sys
from logging import Logger
from typing import List
from penvy.check.CheckInterface import CheckInterface


class ChecksRunner:
    def __init__(
        self,
        checks: List[CheckInterface],
        logger: Logger,
    ):
        self._checks = checks
        self._logger = logger

    def run(self):
        errors = self.check()

        if errors:
            self.print_errors(errors, "Following errors found:")
            sys.exit(1)

    def check(self):
        errors = []

        for check in self._checks:
            check_result = check.run()

            if check_result:
                errors.append(check_result)

        return errors

    def print_errors(self, errors: list, message: str):
        self._logger.error(message)

        for index, error in enumerate(errors):
            self._logger.error(f"{index + 1}. {error}")
