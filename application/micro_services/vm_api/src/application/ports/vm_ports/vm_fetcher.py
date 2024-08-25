# src/application/ports/vm_ports/vm_fetcher.py

from abc import ABC, abstractmethod
from application.micro_services.vm_api.src.domain.models.vm_models.vm_details import VMDetailedInfo

class VMFetcherPort(ABC):
    @abstractmethod
    def fetch(self, vm_id: int) -> VMDetailedInfo:
        pass

