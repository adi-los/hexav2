# src/application/services/kubeconfig_service.py
from application.ports.rancher_ports.kubeconfig import KubeConfigPort
from domain.models.rancher_models.kubeconfig import KubeConfigRequest, KubeConfigResponse

class KubeConfigService:
    def __init__(self, kubeconfig_port: KubeConfigPort):
        self.kubeconfig_port = kubeconfig_port

    def get_kubeconfig(self, request: KubeConfigRequest) -> KubeConfigResponse:
        return self.kubeconfig_port.get_kubeconfig(request)


    def __call__(self):
        return self
