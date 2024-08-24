# src/application/ports/vm_creator.py
from abc import ABC, abstractmethod
class VMRemoverPort(ABC):
    @abstractmethod
    def remove(self):
        pass

