# src/domain/models/node.py
from pydantic import BaseModel

class NodeRegistrationRequest(BaseModel):
    cluster_id: str
    role: str
    ip: str
    username: str
    password: str
