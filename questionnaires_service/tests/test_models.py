import json
import uuid

from src.models.models import QuestionnaireInModel


def test_questionnaire_in_from_json():
    data = {
        "header": "test_header",
        "game": "CS2",
        "description": "test_description",
        "author_id": str(uuid.uuid4())
    }

    json_data = json.dumps(data)
    assert QuestionnaireInModel.model_validate_json(json_data) == QuestionnaireInModel(**data)
