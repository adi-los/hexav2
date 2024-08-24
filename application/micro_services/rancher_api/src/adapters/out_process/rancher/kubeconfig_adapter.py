# src/adapters/out/kubeconfig_adapter.py
import requests
import paramiko
from fastapi import HTTPException
from application.ports.rancher_ports.kubeconfig import KubeConfigPort
from domain.models.rancher_models.kubeconfig import KubeConfigRequest, KubeConfigResponse

class KubeConfigAdapter(KubeConfigPort):
    def __init__(self, api_endpoint: str, access_token: str):
        self.api_endpoint = api_endpoint
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

    def get_kubeconfig(self, request: KubeConfigRequest) -> KubeConfigResponse:
        try:
            url = f"{self.api_endpoint}/clusters/{request.cluster_id}?action=generateKubeconfig"
            response = requests.post(url, headers=self.headers, verify=False)
            response.raise_for_status()
            kubeconfig_content = response.json().get("config")
            if not kubeconfig_content:
                raise HTTPException(status_code=500, detail="Failed to extract kubeconfig content")

            # Copy kubeconfig to the master VM
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(request.master_ip, username=request.username, password=request.password)
            sftp = client.open_sftp()
            try:
                sftp.mkdir('/root/.kube')
            except IOError:
                pass

            kubeconfig_path = '/root/.kube/config'
            with sftp.open(kubeconfig_path, 'w') as f:
                f.write(kubeconfig_content)
            sftp.close()
            client.close()

            return KubeConfigResponse(status="success", path=kubeconfig_path)
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Error fetching kubeconfig: {e}")
        except paramiko.SSHException as e:
            raise HTTPException(status_code=500, detail=f"Error connecting to master VM: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error copying kubeconfig to master VM: {e}")
