from abc import ABC, abstractmethod


class CheckInterface(ABC):
    @abstractmethod
    def run(self):
        pass
