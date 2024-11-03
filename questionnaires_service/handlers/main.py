from __future__ import annotations

from typing import List, Optional, Union

from fastapi import FastAPI, UploadFile

from models import QuestionnaireOut, QuestionnaireIn

app = FastAPI(
    version='1.0.0',
    title='TeamMates questionnaires API',
    contact={'name': 'LongCorp', 'email': 'LongCorp@gmail.com'},
)


@app.get(
    '/questionnaires',
    response_model=List[QuestionnaireOut],
    responses={'400': {'model': str}},
)
def get_questionnaires(
    page: Optional[int] = 1, limit: Optional[int] = 10
) -> Union[List[QuestionnaireOut], str]:
    pass


@app.post(
    '/questionnaires',
    response_model=Optional[QuestionnaireOut],
    responses={'201': {'model': QuestionnaireOut}},
)
def post_questionnaires(questionnaire: QuestionnaireIn) -> Optional[QuestionnaireOut]:
    pass
