import json

from src.models.models import QuestionnaireIn


def test_questionnaire_in_from_json():
    data = {
        "header": "test_header",
        "game": "CS2",
        "description": "test_description",
        "author_id": 1
    }

    json_data = json.dumps(data)
    assert QuestionnaireIn.model_validate_json(json_data) == QuestionnaireIn(**data)
