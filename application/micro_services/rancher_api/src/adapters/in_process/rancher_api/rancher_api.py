


from fastapi import APIRouter, Depends, HTTPException
from application.micro_services.rancher_api.src.domain.models.rancher_models.cluster import CreateClusterRequest
from application.micro_services.rancher_api.src.domain.models.rancher_models.node import NodeRegistrationRequest
from application.micro_services.rancher_api.src.domain.models.rancher_models.kubeconfig import KubeConfigRequest
from common.fetchTemplate import fetchTemplate
from common.http_utils import fetch_json
from application.micro_services.rancher_api.src.domain.services.rancher_injection.service import cluster_svc, node_svc, kubeconfig_svc
import requests

router = APIRouter()





@router.post("/create_cluster")
async def create_cluster(request: CreateClusterRequest, cluster_service=Depends(cluster_svc)):
    print(f"cluster_service: {type(cluster_service)}")
    result = cluster_service.create_cluster(request)
    return result




@router.post("/register_node")
async def register_node(request: NodeRegistrationRequest, node_service=Depends(node_svc.register_node)):
    print(f"node_service: {type(node_service)}")
    result = node_service.register_node(request)
    return result

@router.post("/kubeconfig")
async def get_kubeconfig(request: KubeConfigRequest, kubeconfig_service=Depends(kubeconfig_svc.get_kubeconfig)):
    #return kubeconfig_service(request)
    print(f"kubeconfig_service: {type(kubeconfig_service)}")
    result = kubeconfig_service.get_kubeconfig(request)
    return result


@router.get("/fetch")
async def fetch(commonUse: fetchTemplate):
    # url = "https://jsonplaceholder.typicode.com/todos/1"
    url = commonUse.url
    try:
        data = fetch_json(url)
        return data  # Return the data instead of printing it
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


