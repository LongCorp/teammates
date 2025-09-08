import logging
from uuid import UUID
from starlette.websockets import WebSocket

from src.models.models import MessageModel

logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[UUID, list[WebSocket]] = {}

    async def connect(self, user_id: UUID, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.setdefault(user_id, []).append(websocket)

    async def disconnect(self, user_id: UUID, websocket: WebSocket):
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def send_to_room(self, user_id: UUID, content: MessageModel) -> None:
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                await connection.send_json(data=content.model_dump(by_alias=True, mode="json"))