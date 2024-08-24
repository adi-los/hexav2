# src/application/services/node_service.py
from application.ports.rancher_ports.node_registration import NodeRegistrationPort
from domain.models.rancher_models.node import NodeRegistrationRequest

class NodeService:
    def __init__(self, node_registration_port: NodeRegistrationPort):
        self.node_registration_port = node_registration_port

    def register_node(self, request: NodeRegistrationRequest) -> dict:
        return self.node_registration_port.register_node(request)


    def __call__(self):
        return self
