import uvicorn

from backend.config import Config


if __name__ == "__main__":
    uvicorn.run("backend.app:app", host="0.0.0.0", port=Config.port, reload=False)
