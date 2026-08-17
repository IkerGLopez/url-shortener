import uvicorn
import src.infrastructure.config
from src.infrastructure.adapters.routers.api import app

if __name__ == "__main__":
    print("Iniciando URL Shortener")
    uvicorn.run(app, host="127.0.0.1", port=8000)

