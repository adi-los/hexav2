# src/adapters/out/node_registration_adapter.py
import requests
import paramiko
from fastapi import HTTPException
from application.micro_services.rancher_api.src.application.ports.rancher_ports.node_registration import NodeRegistrationPort
from application.micro_services.rancher_api.src.domain.models.rancher_models.node import NodeRegistrationRequest

class NodeRegistrationAdapter(NodeRegistrationPort):
    def __init__(self, api_endpoint: str, access_token: str):
        self.api_endpoint = api_endpoint
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

    def register_node(self, request: NodeRegistrationRequest) -> dict:
        try:
            url = f"{self.api_endpoint}/clusters/{request.cluster_id}/clusterRegistrationTokens"
            response = requests.get(url, headers=self.headers, verify=False)
            response.raise_for_status()
            registration_command = response.json()['data'][0]['nodeCommand']

            if request.role == 'master':
                command = f"{registration_command} --etcd --controlplane"
            elif request.role == 'worker':
                command = registration_command
            else:
                raise HTTPException(status_code=400, detail="Invalid role specified. Use 'master' or 'worker'.")

            # Execute the command on the remote node
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(request.ip, username=request.username, password=request.password)
            stdin, stdout, stderr = client.exec_command(command)
            output = stdout.read().decode()
            error = stderr.read().decode()
            client.close()

            return {"output": output, "error": error}
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Error fetching registration command: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error executing remote command: {e}")
