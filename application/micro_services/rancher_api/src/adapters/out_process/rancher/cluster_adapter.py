import requests
from fastapi import HTTPException
from application.ports.rancher_ports.cluster_creator import ClusterCreatorPort
from domain.models.rancher_models.cluster import CreateClusterRequest

class ClusterCreatorAdapter(ClusterCreatorPort):
    def __init__(self, api_endpoint: str, access_token: str):
        self.api_endpoint = api_endpoint
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

    def create_cluster(self, request: CreateClusterRequest) -> str:
        payload = {
            "type": "cluster",
            "name": request.name,
            "rancherKubernetesEngineConfig": {
                "kubernetesVersion": request.kubernetes_version,
                "network": {
                    "plugin": request.network_plugin
                },
                "services": {
                    "etcd": {
                        "snapshot": True,
                        "backupConfig": {
                            "enabled": True,
                            "intervalHours": 12,
                            "retention": 6
                        }
                    },
                    "kubeApi": {
                        "podSecurityPolicy": False
                    },
                    "kubeController": {},
                    "scheduler": {},
                    "kubelet": {
                        "failSwapOn": False
                    },
                    "kubeproxy": {}
                },
                "authentication": {
                    "strategy": "x509|webhook"
                },
                "ingress": {
                    "provider": request.ingress_provider
                }
            },
            "defaultPodSecurityPolicyTemplateId": None,
            "enableNetworkPolicy": False,
            "windowsPreferedCluster": False
        }

        try:
            print(f"Sending payload to Rancher API: {payload}")  # Log the payload
            response = requests.post(f"{self.api_endpoint}/clusters", headers=self.headers, json=payload, verify=False)
            response.raise_for_status()
            cluster_id = response.json().get('id')
            if not cluster_id:
                raise HTTPException(status_code=500, detail="No ID returned in response.")
            return cluster_id
        except requests.exceptions.RequestException as e:
            # Log the full response for debugging
            error_detail = response.json() if response.content else str(e)
            print(f"Error response from Rancher API: {error_detail}")  # Log the error response
            raise HTTPException(status_code=500, detail=f"Error creating cluster: {error_detail}")

