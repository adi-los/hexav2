from application.micro_services.rancher_api.src.application.services.rancher_services.cluster import ClusterService
from application.micro_services.rancher_api.src.adapters.out_process.rancher.cluster_adapter import ClusterCreatorAdapter
from application.micro_services.rancher_api.src.application.services.rancher_services.node import NodeService
from application.micro_services.rancher_api.src.adapters.out_process.rancher.registration_adapter import NodeRegistrationAdapter
from application.micro_services.rancher_api.src.application.services.rancher_services.kubeconfig import KubeConfigService
from application.micro_services.rancher_api.src.adapters.out_process.rancher.kubeconfig_adapter import KubeConfigAdapter
import os
from pathlib import Path


from environs import Env

env = Env()
env.read_env(path='/root/hexav2/application/micro_services/rancher_api/src/config/vars/.env')  # Specify the path to the .env file

endpoint = env.str('ENDPOINT')

token = env.str('TOKEN')


# Dependency injection
cluster_svc = ClusterService(
    cluster_creator_port=ClusterCreatorAdapter(api_endpoint=endpoint, access_token=token)
)
node_svc = NodeService(
    node_registration_port=NodeRegistrationAdapter(api_endpoint=endpoint, access_token=token)
)
kubeconfig_svc = KubeConfigService(
    kubeconfig_port=KubeConfigAdapter(api_endpoint=endpoint, access_token=token)
)

