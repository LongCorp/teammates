import uuid
from src.utils.utils import get_validated_user_dict_from_tuple


def test_get_validated_user_dict_from_tuple():
    test_uuid = str(uuid.uuid4())
    data = (1, test_uuid, "test_nick", "test@email.com", "test_description", "test_image_path")
    expected = {
        'public_id': 1,
        'secret_id': test_uuid,
        'nickname': "test_nick",
        "email": "test@email.com",
        'description': "test_description",
        'image_path': "test_image_path",
    }
    assert get_validated_user_dict_from_tuple(data) == expected
