# src/domain/models/kubeconfig.py
from pydantic import BaseModel

class KubeConfigRequest(BaseModel):
    master_ip: str
    username: str
    password: str
    cluster_id: str

class KubeConfigResponse(BaseModel):
    status: str
    path: str
