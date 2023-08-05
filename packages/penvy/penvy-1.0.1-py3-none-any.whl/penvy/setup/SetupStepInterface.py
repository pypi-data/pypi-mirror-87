from abc import ABC, abstractmethod


class SetupStepInterface(ABC):
    @abstractmethod
    def get_description(self):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def should_be_run(self) -> bool:
        pass
