import asyncio

from uvicorn import Config, Server

from app import create_app
from core.config import settings
from core.logger import get_logger

logger = get_logger(__name__)
app = create_app()


async def run():
    config = Config(app, host="0.0.0.0", port=settings.PORT)
    server = Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(run())
