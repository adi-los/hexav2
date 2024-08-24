# src/domain/models/vm_models/vm_details.py
from pydantic import BaseModel

class VMDetailedInfo(BaseModel):
    id: int
    name: str
    status: str
    memory: int
    vcpus: int
    disk_size: int
    image_path: str

