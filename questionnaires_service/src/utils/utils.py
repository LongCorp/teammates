import logging
from uuid import UUID
import os
import aiofiles
from fastapi import UploadFile

logger = logging.getLogger(__name__)


async def save_questionnaire_image(image: UploadFile | None, questionnaire_id: UUID, start_path: str) -> str:
    if image:
        try:
            path = os.path.abspath(f"./questionnaires_photos/{questionnaire_id}.jpg")
            if not os.path.exists("./questionnaires_photos"):
                os.mkdir("./questionnaires_photos/")
            async with aiofiles.open(path, "wb") as out_file:
                content = await image.read()
                await out_file.write(content)
            server_path = "/".join(start_path.split("/")[:-1]) + f"/questionnaires_photos/{questionnaire_id}.jpg"
            return server_path
        except Exception as e:
            logger.error("Error while saving image", exc_info=e)
            return ""
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


def create_logs_folder():
    log_dir = "logs/"
    log_file = os.path.join(log_dir, "service.log")

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    if not os.path.exists(log_file):
        with open(log_file, "w") as f:
            f.write("")
