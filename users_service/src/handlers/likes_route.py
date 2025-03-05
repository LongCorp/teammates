import json
import logging
from uuid import UUID

from fastapi import APIRouter, HTTPException
from starlette.responses import Response

from src.database import likes_methods, questionnaires_methods, users_methods

from src.models.models import UserLikeModel, QuestionnaireLikeModel, QuestionnaireOut, UserModel

logger = logging.getLogger(__name__)


likes_router = APIRouter()


@likes_router.get("/like/questionnaires")
async def get_liked_questionnaires(user_id: UUID) -> list[QuestionnaireOut]:
    questionnaires = await likes_methods.get_liked_questionnaires(liker_id=user_id)
    return questionnaires


@likes_router.get("/like/users")
async def get_liked_users(user_id: UUID) -> list[UserModel]:
    users_info = await likes_methods.get_liked_users(liker_id=user_id)
    return users_info


@likes_router.post("/like/questionnaire")
async def like_questionnaire(user_id: UUID, like_info: QuestionnaireLikeModel) -> Response:
    liker_id, questionnaire_id = like_info.liker_id, like_info.questionnaire_id
    logger.info("Received a request to like questionnaire %s by user %s", questionnaire_id, liker_id)

    if user_id == liker_id:
        questionnaire = await questionnaires_methods.get_questionnaire(questionnaire_id=questionnaire_id)
        like = await likes_methods.check_questionnaire_like(liker_id=liker_id, questionnaire_id=questionnaire_id)
        if questionnaire and like:
            logger.info("User %s already liked questionnaire %s", liker_id, questionnaire_id)
            return Response(
                status_code=200,
                content=json.dumps({
                    "message": "Questionnaire already liked"
                })
            )

        if questionnaire:
            await likes_methods.add_like_to_questionnaire(liker_id=liker_id, questionnaire_id=questionnaire_id)
            logger.info("User %s successfully liked questionnaire %s", liker_id, questionnaire_id)
            return Response(
                status_code=201,
                content=json.dumps({
                    "message": "Questionnaire was successfully liked",
                    "liker_id": str(liker_id),
                    "questionnaire_id": str(questionnaire_id)
                })
            )

        raise HTTPException(404, f"Error while liking questionnaire {questionnaire_id} by user {liker_id}")
    logger.error("user_id %s and liker_id %s did not match", user_id, liker_id)
    raise HTTPException(400, "user_id and liker_id must be the same")



@likes_router.post("/like/user")
async def like_user(user_id: UUID, like_info: UserLikeModel) -> Response:
    liker_id, liked_id = like_info.liked_by_id, like_info.liked_id
    logger.info("Received a request to like user %s by user %s", liked_id, liker_id)
    if user_id == liker_id:
        if liker_id == liked_id:
            logger.info("User %s tried to like himself", liker_id)
            raise HTTPException(400, detail="You cannot like yourself")

        user = await users_methods.get_user_by_public_id(public_id=liked_id)
        like = await likes_methods.check_user_like(liker_id=liker_id, liked_id=liked_id)
        if like and user:
            logger.info("User %s already liked user %s", liker_id, liked_id)
            return Response(
                status_code=200,
                content=json.dumps({
                    "message": "User already liked"
                })
            )

        if user:
            await likes_methods.add_like_to_user(liker_id=liker_id, liked_id=liked_id)
            logger.info("User %s successfully liked user %s", liker_id, liked_id)
            return Response(
                status_code=201,
                content=json.dumps({
                    "message": "User was successfully liked",
                    "liker_id": str(liker_id),
                    "liked_user_id": str(liked_id)
                })
            )

        raise HTTPException(404, f"Error while liking user {liked_id} by user {liker_id}")
    logger.error("user_id %s and liker_id %s did not match", user_id, liker_id)
    raise HTTPException(400, "user_id and liker_id must be the same")



@likes_router.delete("/like/questionnaire")
async def delete_like_questionnaire(user_id: UUID, like_info: QuestionnaireLikeModel) -> Response:
    liker_id, questionnaire_id = like_info.liker_id, like_info.questionnaire_id
    logger.info("Received user %s request to delete questionnaire %s like", liker_id, questionnaire_id)
    if user_id == liker_id:
        like = await likes_methods.check_questionnaire_like(liker_id=liker_id, questionnaire_id=questionnaire_id)
        if like:
            await likes_methods.delete_liked_questionnaire(liker_id=liker_id, questionnaire_id=questionnaire_id)
            logger.info("Users %s like for questionnaire %s successfully deleted", liker_id, questionnaire_id)
            return Response(
                status_code=200,
                content=json.dumps({
                    "message": "Like successfully deleted",
                    "liker_id": str(liker_id),
                    "questionnaire_id": str(questionnaire_id)
                })
            )
        logger.info("Users %s like for questionnaire %s was deleted previously or never existed", liker_id, questionnaire_id)
        return Response(
            status_code=200,
            content=json.dumps({
                "message": "Like was deleted previously or never existed",
                "liker_id": str(liker_id),
                "questionnaire_id": str(questionnaire_id)
            })
        )
    logger.error("User_id %s and liker_id %s did not match", user_id, liker_id)
    raise HTTPException(400, "user_id and liker_id must be the same")

@likes_router.delete("/like/user")
async def delete_like_user(user_id: UUID, like_info: UserLikeModel) -> Response:
    liker_id, liked_id = like_info.liked_by_id, like_info.liked_id
    logger.info("Received user %s request to delete like for user %s", liker_id, liked_id)
    if user_id == liker_id:
        like_exists = await likes_methods.check_user_like(liker_id=liker_id, liked_id=liked_id)
        if like_exists:
            await likes_methods.delete_liked_user(liker_id=liker_id, liked_id=liked_id)
            logger.info("Users %s like for user %s successfully deleted", liker_id, liked_id)
            return Response(
                status_code=200,
                content=json.dumps({
                    "message": "Like successfully deleted",
                    "liker_id": str(liker_id),
                    "liked_user_id": str(liked_id)
                })
            )
        logger.info("Users %s like for user %s was deleted previously or never existed", liker_id, liked_id)
        return Response(
            status_code=200,
            content=json.dumps({
                "message": "Like was deleted previously or never existed",
                "liker_id": str(liker_id),
                "liked_user_id": str(liked_id)
            })
        )
    logger.error("User_id %s and liker_id %s did not match", user_id, liker_id)
    raise HTTPException(400, "user_id and liker_id must be the same")