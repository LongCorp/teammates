import asyncio

import uvicorn

from src.handlers.auth_api import app


async def main():
    config = uvicorn.Config(app=app, host="0.0.0.0", port=8100, loop="asyncio", reload=True)
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == '__main__':
    asyncio.run(main())
