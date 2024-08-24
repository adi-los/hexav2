# src/application/ports/node_registration.py
from abc import ABC, abstractmethod
from domain.models.rancher_models.node import NodeRegistrationRequest

class NodeRegistrationPort(ABC):
    @abstractmethod
    def register_node(self, request: NodeRegistrationRequest) -> dict:
        pass
