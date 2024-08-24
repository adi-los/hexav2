from pydantic import BaseModel

class VMCreateRequest(BaseModel):
    addressip: str
    hostname: str
    gateway: str
    nameserver: str
    RAM: int
    CPU: int
    hostnamevm: str
    size: int
    proxy: str
    network: str
    tenant_name: str
    template_name: str