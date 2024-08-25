# src/application/use_cases/create_vm.py
from application.micro_services.vm_api.src.domain.models.vm_models.vm_model import VMCreateRequest
from application.micro_services.vm_api.src.application.ports.vm_ports.vm_creator import VMCreatorPort

class CreateVMUseCase:
    def __init__(self, vm_creator: VMCreatorPort):
        self.vm_creator = vm_creator

    def execute(self, vm_request: VMCreateRequest):
        # Business logic, e.g., validation, before passing to the VM creator
        self.vm_creator.create(vm_request)
