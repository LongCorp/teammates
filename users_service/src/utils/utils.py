import logging
import os
from uuid import UUID

import aiofiles
from fastapi import UploadFile


logger = logging.getLogger(__name__)

def get_validated_user_dict_from_tuple(data: tuple) -> dict:
    public_id, secret_id, nickname, email, description, image_path = data
    return {
        'public_id': public_id,
        'secret_id': secret_id,
        'nickname': nickname,
        'email': email,
        'description': description,
        'image_path': image_path
    }

def get_validated_questionnaire_dict_from_tuple(data: tuple) -> dict:
    author_id, questionnaire_id, header, description, photo_path, game = data
    return {
        'header': header,
        'questionnaire_id': questionnaire_id,
        'photo_path': photo_path,
        'description': description,
        'author_id': author_id,
        'game': game
    }

async def save_profile_photo(image: UploadFile | None, user_id: UUID, start_path: str) -> str:
    if image:
        try:
            path = os.path.abspath(f"./profile_photos/{user_id}.jpg")
            if not os.path.exists("./profile_photos"):
                os.mkdir("./profile_photos/")
            async with aiofiles.open(path, "wb") as out_file:
                content = await image.read()
                await out_file.write(content)
            server_path = "/".join(start_path.split("/")[:-2]) + f"/profile_photos/{user_id}.jpg"
            return server_path
        except Exception as e:
            logger.error("Error while saving image", exc_info=e)
            return ""
    return ""
