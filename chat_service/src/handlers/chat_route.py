import json
import logging

from fastapi import APIRouter
from uuid import UUID
from starlette.websockets import WebSocket, WebSocketDisconnect

from src.models.models import MessageModel
from src.services.chat_manager import ConnectionManager


logger = logging.getLogger(__name__)
chat_router = APIRouter(
    prefix="/chat",
)

manager = ConnectionManager()


@chat_router.websocket("/ws")
async def chat_websocket(
        websocket: WebSocket,
        user_id: UUID
    ):
    try:
        await manager.connect(user_id, websocket)

        while True:
            data = await websocket.receive_json()
            receiver_id = UUID(data.get("receiver_id"))

            content = MessageModel(**data)

            await manager.send_to_room(receiver_id, content)
    except WebSocketDisconnect:
        await manager.disconnect(user_id, websocket)
    except Exception as e:
        logger.error(" WebSocket for %s:", user_id, exc_info=e)
        await manager.disconnect(user_id, websocket)
        await websocket.close()
