from os import getenv

from uvicorn import run
from dotenv import load_dotenv

load_dotenv()


ENVIRONMENT = getenv("ENVIRONMENT")
PORT = int(getenv("PORT", "8080"))

if __name__ == "__main__":
    run(
        "src.main.config.http_server_configs:app",
        host="0.0.0.0",
        port=PORT,
        reload=(ENVIRONMENT == "DEV"),
        debug=(ENVIRONMENT == "DEV"),
    )
