from abc import ABC, abstractmethod
from domain.models.rancher_models.cluster import CreateClusterRequest

class ClusterCreatorPort(ABC):
    @abstractmethod
    def create_cluster(self, request: CreateClusterRequest) -> str:
        pass
