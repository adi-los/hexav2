# src/application/ports/kubeconfig.py
from abc import ABC, abstractmethod
from application.micro_services.rancher_api.src.domain.models.rancher_models.kubeconfig import KubeConfigRequest, KubeConfigResponse

class KubeConfigPort(ABC):
    @abstractmethod
    def get_kubeconfig(self, request: KubeConfigRequest) -> KubeConfigResponse:
        pass
