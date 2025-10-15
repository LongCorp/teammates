import logging
from typing import Dict
from uuid import UUID

from pydantic import BaseModel, create_model, ValidationError
from starlette.websockets import WebSocket

from src.database import messages_methods
from src.models.models import NewMessageModel, ReadMessageModel, UpdatedMessageModel, DeletedMessageModel, ErrorModel

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

    async def send_to_client(self, user_id: UUID, content: BaseModel) -> None:
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                await connection.send_json(data=content.model_dump(by_alias=True, mode="json"))


class EventHandler:

    def __init__(self, websocket: WebSocket, manager: ConnectionManager):
        self.websocket = websocket
        self.manager = manager


        self.handlers_types = {
            "new_message": {"handler": self.handle_new_message, "model": NewMessageModel},
            "read_message": {"handler": self.handle_read_message, "model": ReadMessageModel},
            "edit_message": {"handler": self.handle_edited_message, "model": UpdatedMessageModel},
            "delete_message": {"handler": self.handle_deleted_message, "model": DeletedMessageModel},
        }

    async def dispatch(self, data: Dict[str, str], user_id: UUID):
        try:
            msg_type = data.get("msg_type")
            handler_dict = self.handlers_types.get(msg_type)
            if handler_dict:
                handler = self.handlers_types.get(msg_type).get("handler")
                msg_model = self.handlers_types.get(msg_type).get("model")
                message = msg_model.model_validate(data)
                if message.sender_id == message.receiver_id or message.sender_id != user_id:
                    raise ValueError
                await self.manager.send_to_client(
                    user_id=message.receiver_id,
                    content=message
                )
                return await handler(message=msg_model.model_validate(data))
            else:
                raise ValueError
        except (ValidationError, ValueError) as e:
            await self.manager.send_to_client(
                user_id=user_id,
                content=ErrorModel(data=data, error_msg="Message was not validated")
            )
            logger.error(data, exc_info=e)
            return None

    async def handle_new_message(self, message: NewMessageModel) -> None:

        # {
        #     "sender_id": "...",
        #     "receiver_id": "...",
        #     "msg_type": "new_message",
        #     "content": "..."
        # }
        await messages_methods.add_message_to_database(message)

    async def handle_read_message(self, message: ReadMessageModel) -> None:
        # {
        #     "sender_id": "...",
        #     "receiver_id": "...",
        #     "msg_type": "read_message",
        #     "message_id": "..."
        # }
        await messages_methods.update_read_message(message)

    async def handle_edited_message(self, message: UpdatedMessageModel) -> None:
        # {
        #     "sender_id": "...",
        #     "receiver_id": "...",
        #     "msg_type": "edit_message",
        #     "content": "...",
        #     "message_id": "..."
        # }
        await messages_methods.update_edited_message(message)

    async def handle_deleted_message(self, message: DeletedMessageModel) -> None:
        # {
        #     "sender_id": "...",
        #     "receiver_id": "...",
        #     "msg_type": "delete_message",
        #     "content": "..."
        # }
        await messages_methods.delete_message(message)

