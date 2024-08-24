# src/application/services/cluster_service.py
from application.ports.rancher_ports.cluster_creator import ClusterCreatorPort
from domain.models.rancher_models.cluster import CreateClusterRequest

class ClusterService:
    def __init__(self, cluster_creator_port: ClusterCreatorPort):
        self.cluster_creator_port = cluster_creator_port

    def create_cluster(self, request: CreateClusterRequest) -> str:
        return self.cluster_creator_port.create_cluster(request)


    def __call__(self):
        return self
