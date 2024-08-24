
# src/adapters/in/api.py
from fastapi import HTTPException, APIRouter
from domain.models.vm_models.vm_model import VMCreateRequest
from application.services.vm_services.create_vm import CreateVMUseCase
from application.services.vm_services.remove_vm import RemoveVMUseCase
from adapters.out_process.virt.virt_adapter import VirtInstallVMCreator
from adapters.out_process.virt.virt_adapter import VirtInstallVMRemover
from domain.models.vm_models.vm_details import VMDetailedInfo
from application.services.vm_services.get_vm import GetVMUseCase
from adapters.out_process.virt.virt_adapter import VirtInstallVMFetcher 
from fastapi import APIRouter
from dotenv import load_dotenv
import requests
from dommon.fetchTemplate import fetchTemplate
from common.http_utils import fetch_json
from dotenv import load_dotenv
import os
from pathlib import Path

# Define the relative path to your .env file
env_path = Path('config/vars/.env')

# Load the .env file
load_dotenv(dotenv_path=env_path)

images_dir = os.getenv("IMAGES_DIR")
templates_dir = os.getenv("TEMPLATES_PATH")

router = APIRouter()

vm_creator = VirtInstallVMCreator(templates_dir)
create_vm_use_case = CreateVMUseCase(vm_creator)

@router.post("/create_vm")
async def create_vm(vm_request: VMCreateRequest):
    try:
        create_vm_use_case.execute(vm_request)
        return {"message": f"Virtual machine {vm_request.hostnamevm} created successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    




image_directory = images_dir


vm_remover = VirtInstallVMRemover(image_directory)
remove_vm_use_case = RemoveVMUseCase(vm_remover)
@router.delete("/vms/{vm_id}")
async def delete_vm(vm_id: int):
    try:
        remove_vm_use_case.execute(vm_id)
        return {"message": f"Virtual machine with {vm_id} removed successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




vm_getter = VirtInstallVMFetcher(str(image_directory))
get_vm_use_case = GetVMUseCase(vm_getter)
@router.get("/vms/{vm_id}", response_model=VMDetailedInfo)
async def fetch(vm_id: int):
    try:
        vm_details = get_vm_use_case.execute(vm_id)
        return vm_details
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





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


