import shutil
import uuid

import pytest
from src.utils.utils import save_questionnaire_image, get_validated_dict_from_tuple
from fastapi import UploadFile
from tempfile import TemporaryFile


@pytest.mark.parametrize(
    "image, questionnaire_id, start_path, expected",
    [
        (None, "test_uuid", "start_path", ""),
        ("wrong_image", "test_uuid", "start_path", ""),
    ]
)
@pytest.mark.asyncio
async def test_save_questionnaire_image_return_empty(image, questionnaire_id, start_path, expected):
    result = await save_questionnaire_image(image, questionnaire_id, start_path)
    assert result == expected


@pytest.mark.asyncio
async def test_save_questionnaire_image_return_path():
    file = UploadFile(file=TemporaryFile(), filename="test.jpg")
    questionnaire_id = uuid.uuid4()
    start_path = "test_service/test_path"

    expected = f"test_service/questionnaires_photos/{questionnaire_id}.jpg"
    result = await save_questionnaire_image(file, questionnaire_id, start_path)
    assert result == expected
    if result:
        shutil.rmtree("./questionnaires_photos")


def test_get_validated_user_dict_from_tuple():
    test_uuid = str(uuid.uuid4())
    data = (1, test_uuid, "test_header", "test_description", "test_photo_path", "CS2")
    expected = {
        'header': 'test_header',
        'questionnaire_id': test_uuid,
        'photo_path': "test_photo_path",
        'description': "test_description",
        'author_id': 1,
        'game': "CS2",
    }
    assert get_validated_dict_from_tuple(data) == expected
