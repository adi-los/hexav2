# src/application/services/vm_services/get_vm.py

from application.micro_services.vm_api.src.domain.models.vm_models.vm_details import VMDetailedInfo
from application.micro_services.vm_api.src.application.ports.vm_ports.vm_fetcher import VMFetcherPort  # Import the port interface

class GetVMUseCase:
    def __init__(self, vm_getter: VMFetcherPort):  # Use the port interface here
        self.vm_getter = vm_getter

    def execute(self, vm_id: int) -> VMDetailedInfo:
        # Fetch VM details
        vm_data = self.vm_getter.fetch(vm_id)

        # Create and return VMDetailedInfo instance
        return VMDetailedInfo(
            id=vm_data.id,  # Access directly if vm_data is a VMDetailedInfo instance
            name=vm_data.name,
            status=vm_data.status,  # Ensure status is a string
            memory=vm_data.memory,
            vcpus=vm_data.vcpus,
            disk_size=vm_data.disk_size,
            image_path=vm_data.image_path
        )

