# src/application/ports/vm_creator.py
from abc import ABC, abstractmethod
from application.micro_services.vm_api.src.domain.models.vm_models.vm_model import VMCreateRequest

class VMCreatorPort(ABC):
    @abstractmethod
    def create(self, vm_request: VMCreateRequest):
        pass
