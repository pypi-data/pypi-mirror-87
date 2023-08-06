from abc import ABC, abstractmethod


class TearDownStepInterface(ABC):
    @abstractmethod
    def run(self):
        pass
