from backend.app import app
from backend.config import Config


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.port)
