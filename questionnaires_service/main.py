import asyncio
import logging

import uvicorn

from src.entities.entities import LoggerHandlers
from src.handlers.questionnaires_api import app


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s] %(module)s:%(lineno)d %(levelname)7s - %(message)s",
        handlers=[LoggerHandlers.file_handler, LoggerHandlers.console_handler]
    )


async def main():
    configure_logging()
    config = uvicorn.Config(app=app, host="0.0.0.0", port=8000, loop="asyncio", reload=True)
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == '__main__':
    asyncio.run(main())
