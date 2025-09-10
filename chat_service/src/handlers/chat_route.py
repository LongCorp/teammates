import json
import logging
from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, Query
from uuid import UUID
from starlette.websockets import WebSocket, WebSocketDisconnect

from src.database import messages_methods
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
            await messages_methods.add_message_to_database(content)
    except WebSocketDisconnect:
        await manager.disconnect(user_id, websocket)
    except Exception as e:
        logger.error(" WebSocket for %s:", user_id, exc_info=e)
        await manager.disconnect(user_id, websocket)
        await websocket.close()


@chat_router.get("/messages", response_model=List[MessageModel])
async def get_chat_messages(
    user_id: UUID,
    peer_id: UUID,
    limit: int = Query(20, ge=1, le=100),
    before: Optional[datetime] = None,
):
    messages = await messages_methods.get_chat_messages(
        user_id=user_id,
        peer_id=peer_id,
        limit=limit,
        before=before
    )
    return messages


@chat_router.post("/read")
async def read_chat_message(
        user_id: UUID,
        message_id: UUID,
):
    status = await messages_methods.mark_read_message(user_id, message_id)
    if status:
        return {"status": "success"}
    return {"status": "failed"}
