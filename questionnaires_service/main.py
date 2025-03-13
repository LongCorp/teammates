import asyncio
import logging
import os

import uvicorn

from src.utils.utils import create_logs_folder
from src.handlers.main_route import app
from src.handlers.questionnaire_route import questionnaire_router
from src.handlers.questionnaires_route import questionnaires_router


def configure_logging():
    create_logs_folder()
    file_handler = logging.FileHandler("./logs/service.log")
    console_handler = logging.StreamHandler()
    logging.basicConfig(
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s] %(module)9s:%(lineno)3d %(levelname)5s - %(message)s",
        handlers=[file_handler, console_handler]
    )


async def main():
    app.include_router(questionnaires_router)
    app.include_router(questionnaire_router)
    configure_logging()
    config = uvicorn.Config(app=app, host="0.0.0.0", port=8000, loop="asyncio", reload=True)
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == '__main__':
    asyncio.run(main())
