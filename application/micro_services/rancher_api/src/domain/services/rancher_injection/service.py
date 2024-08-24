from application.services.rancher_services.cluster import ClusterService
from adapters.out_process.rancher.cluster_adapter import ClusterCreatorAdapter
from application.services.rancher_services.node import NodeService
from adapters.out_process.rancher.registration_adapter import NodeRegistrationAdapter
from application.services.rancher_services.kubeconfig import KubeConfigService
from adapters.out_process.rancher.kubeconfig_adapter import KubeConfigAdapter
from dotenv import load_dotenv
import os
from pathlib import Path

# Define the relative path to your .env file
env_path = Path('config/vars/.env')

# Load the .env file
load_dotenv(dotenv_path=env_path)

endpoint = os.getenv("ENDPOINT")
token = os.getenv("TOKEN")


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

