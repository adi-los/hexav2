# src/domain/models/cluster.py
from pydantic import BaseModel

class CreateClusterRequest(BaseModel):
    name: str
    kubernetes_version: str
    network_plugin: str
    ingress_provider: str
