import json
import logging
from uuid import UUID

from fastapi import APIRouter, HTTPException
from starlette.responses import Response

from src.entities.entities import DBEntities
from src.models.models import UserLikeModel, QuestionnaireLikeModel


logger = logging.getLogger(__name__)


likes_router = APIRouter()


@likes_router.get("/like/questionnaires")
async def get_liked_questionnaires(user_id: int) -> list:
    questionnaires = await DBEntities.liked_questionnaires_db.get_liked_questionnaires(user_id)
    return questionnaires

@likes_router.get("/like/users")
async def get_liked_users(user_id: int) -> list:
    users_info = await DBEntities.liked_users_db.get_liked_users(user_id)
    return users_info


@likes_router.post("/like/questionnaire")
async def like_questionnaire(user_id: int, like_info: QuestionnaireLikeModel) -> Response:
    liker_id, questionnaire_id = like_info.liker_id, like_info.questionnaire_id
    logger.info("Received a request to like questionnaire %s by user %s", questionnaire_id, liker_id)
    if user_id == liker_id:
        questionnaire_exists = await DBEntities.questionnaires_db.check_existing(questionnaire_id)
        like_exists = await DBEntities.liked_questionnaires_db.check_existing(liker_id, questionnaire_id)
        if questionnaire_exists and like_exists:
            logger.info("User %s already liked questionnaire %s", liker_id, questionnaire_id)
            return Response(
                status_code=200,
                content=json.dumps({
                    "message": "Questionnaire already liked"
                })
            )

        if questionnaire_exists:
            await DBEntities.liked_questionnaires_db.add_questionnaire(liker_id, questionnaire_id)
            logger.info("User %s successfully liked questionnaire %s", liker_id, questionnaire_id)
            return Response(
                status_code=201,
                content=json.dumps({
                    "message": "Questionnaire was successfully liked",
                    "liker_id": liker_id,
                    "questionnaire_id": str(questionnaire_id)
                })
            )

        raise HTTPException(404, f"Error while liking questionnaire {questionnaire_id} by user {liker_id}")
    logger.error("user_id %s and liker_id %s did not match", user_id, liker_id)
    raise HTTPException(400, "user_id and liker_id must be the same")



@likes_router.post("/like/user")
async def like_user(user_id: int, like_info: UserLikeModel) -> Response:
    liker_id, liked_id = like_info.liker_id, like_info.liked_id
    logger.info("Received a request to like user %s by user %s", liked_id, liker_id)
    if user_id == liker_id:
        if liker_id == liked_id:
            logger.info("User %s tried to like himself", liker_id)
            raise HTTPException(400, detail="You cannot like yourself")

        liked_user_exists = await DBEntities.users_db.get_user_by_public_id(liked_id)
        like_exists = await DBEntities.liked_users_db.check_existing(liker_id, liked_id)
        if like_exists and liked_user_exists:
            logger.info("User %s already liked user %s", liker_id, liked_id)
            return Response(
                status_code=200,
                content=json.dumps({
                    "message": "User already liked"
                })
            )


        if liked_user_exists:
            await DBEntities.liked_users_db.add_user(liker_id, liked_id)
            logger.info("User %s successfully liked user %s", liker_id, liked_id)
            return Response(
                status_code=201,
                content=json.dumps({
                    "message": "User was successfully liked",
                    "liker_id": liker_id,
                    "liked_user_id": liked_id
                })
            )

        raise HTTPException(404, f"Error while liking user {liked_id} by user {liker_id}")
    logger.error("user_id %s and liker_id %s did not match", user_id, liker_id)
    raise HTTPException(400, "user_id and liker_id must be the same")



@likes_router.delete("/like/questionnaire")
async def delete_like_questionnaire(user_id: int, like_info: QuestionnaireLikeModel) -> Response:
    liker_id, questionnaire_id = like_info.liker_id, like_info.questionnaire_id
    logger.info("Received user %s request to delete questionnaire %s like", liker_id, questionnaire_id)
    if user_id == liker_id:
        like_exists = await DBEntities.liked_questionnaires_db.check_existing(liker_id, questionnaire_id)
        if like_exists:
            await DBEntities.liked_questionnaires_db.delete_questionnaire(liker_id, questionnaire_id)
            logger.info("Users %s like for questionnaire %s successfully deleted", liker_id, questionnaire_id)
            return Response(
                status_code=200,
                content=json.dumps({
                    "message": "Like successfully deleted",
                    "liker_id": liker_id,
                    "questionnaire_id": str(questionnaire_id)
                })
            )
        logger.info("Users %s like for questionnaire %s was deleted previously or never existed", liker_id, questionnaire_id)
        return Response(
            status_code=200,
            content=json.dumps({
                "message": "Like was deleted previously or never existed",
                "liker_id": liker_id,
                "questionnaire_id": str(questionnaire_id)
            })
        )
    logger.error("User_id %s and liker_id %s did not match", user_id, liker_id)
    raise HTTPException(400, "user_id and liker_id must be the same")

@likes_router.delete("/like/user")
async def delete_like_user(user_id: int, like_info: UserLikeModel) -> Response:
    liker_id, liked_id = like_info.liker_id, like_info.liked_id
    logger.info("Received user %s request to delete like for user %s", liker_id, liked_id)
    if user_id == liker_id:
        like_exists = await DBEntities.liked_users_db.check_existing(liker_id, liked_id)
        if like_exists:
            await DBEntities.liked_users_db.delete_user(liker_id, liked_id)
            logger.info("Users %s like for user %s successfully deleted", liker_id, liked_id)
            return Response(
                status_code=200,
                content=json.dumps({
                    "message": "Like successfully deleted",
                    "liker_id": liker_id,
                    "liked_user_id": liked_id
                })
            )
        logger.info("Users %s like for user %s was deleted previously or never existed", liker_id, liked_id)
        return Response(
            status_code=200,
            content=json.dumps({
                "message": "Like was deleted previously or never existed",
                "liker_id": liker_id,
                "liked_user_id": liked_id
            })
        )
    logger.error("User_id %s and liker_id %s did not match", user_id, liker_id)
    raise HTTPException(400, "user_id and liker_id must be the same")