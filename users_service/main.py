import asyncio
import logging

import uvicorn

from src.entities.entities import LoggerHandlers
from src.handlers.main_route import app
from src.handlers.likes_route import likes_router
from src.handlers.users_route import users_router

def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s] %(module)9s:%(lineno)3d %(levelname)5s - %(message)s",
        handlers=[LoggerHandlers.file_handler, LoggerHandlers.console_handler]
    )

async def main():
    app.include_router(likes_router)
    app.include_router(users_router)
    configure_logging()
    config = uvicorn.Config(app=app, host="0.0.0.0", port=8200, loop="asyncio", reload=True)
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())