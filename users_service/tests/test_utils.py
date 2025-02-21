from src.utils.utils import get_validated_user_dict_from_tuple, get_validated_questionnaire_dict_from_tuple


def test_validating_user_dict_from_valid_tuple():
    data = (1, "uuid", "user", "aboba@mail.ru", "description", "path_to_image")
    expected_output = {
        'public_id': 1,
        'secret_id': "uuid",
        'nickname': "user",
        "email": "aboba@mail.ru",
        'description': "description",
        'image_path': "path_to_image"
    }
    assert get_validated_user_dict_from_tuple(data) == expected_output

def test_validating_questionnaire_from_valid_tuple():
    data = (1, "uuid", "header", "description", "path_to_photo", "game")
    expected_output = {
        "author_id": 1,
        "questionnaire_id":"uuid",
        "photo_path": "path_to_photo",
        "description": "description",
        "header": "header",
        "game": "game"
    }
    assert get_validated_questionnaire_dict_from_tuple(data) == expected_output