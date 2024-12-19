from uuid import UUID
import os

import aiofiles
from fastapi import UploadFile


async def save_questionnaire_image(image: UploadFile | None, questionnaire_id: UUID) -> str:
    if image:
        path = os.path.abspath(f"./questionnaires_photos/{questionnaire_id}.jpg")
        async with aiofiles.open(path, "wb") as out_file:
            content = await image.read()
            await out_file.write(content)
        return path
    return ""


def get_validated_dict_from_tuple(data: tuple) -> dict:
    author_id, questionnaire_id, header, description, photo_path, game = data
    return {
        'header': header,
        'questionnaire_id': questionnaire_id,
        'photo_path': photo_path,
        "description": description,
        'author_id': author_id,
        'game': game
    }
