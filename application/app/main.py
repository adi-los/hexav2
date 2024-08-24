import uvicorn
# import sys
# from pathlib import Path
# sys.path.append(str(Path(__file__).resolve().parent))
from api_v1 import app
# from adapters.in_process.vm_api.vm_api import app

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)


