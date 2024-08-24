from application.ports.vm_ports.vm_remover import VMRemoverPort

class RemoveVMUseCase:
    def __init__(self, vm_remover: VMRemoverPort):
        self.vm_remover = vm_remover

    def execute(self, vm_id: int):
        # Business logic, e.g., validation, before passing to the VM remover
        self.vm_remover.remove(vm_id)  # Corrected method call

