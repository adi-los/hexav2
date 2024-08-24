
from fastapi import FastAPI

from micro_services.vm_api.src.adapters.in_process.vm_api.vm_api import router as vm_router
from micro_services.rancher_api.src.adapters.in_process.rancher_api.rancher_api import router as rancher_router

app = FastAPI()

app.include_router(rancher_router, prefix="/api")
app.include_router(vm_router, prefix="/api")

