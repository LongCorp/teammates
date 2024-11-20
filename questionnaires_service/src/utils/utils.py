from uuid import UUID
import os

import aiofiles
from fastapi import UploadFile


async def save_questionnaire_image(image: UploadFile | None, questionnaire_id: UUID) -> str:
    if image:
        path = os.path.abspath(f"../questionnaires_photos/{questionnaire_id}.jpg")
        async with aiofiles.open(path, "wb") as out_file:
            content = await image.read()
            await out_file.write(content)
        return path
    return ""
