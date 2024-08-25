from abc import ABC, abstractmethod
from application.micro_services.rancher_api.src.domain.models.rancher_models.cluster import CreateClusterRequest

class ClusterCreatorPort(ABC):
    @abstractmethod
    def create_cluster(self, request: CreateClusterRequest) -> str:
        pass
