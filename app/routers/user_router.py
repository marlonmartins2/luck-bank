import logging

from fastapi import APIRouter, status, Depends, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from models.users import (
    User,
    UserCreateRequest,
    UserResponse,
    StatusEnum,
)

from database.controllers import UserController

logger = logging.getLogger("UserLogger")


user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreateRequest, background_tasks: BackgroundTasks):
    """
    Create user\n
    Args:\n
        user (UserCreateRequest): User data\n
        background_tasks (BackgroundTasks): Background tasks\n
    Returns:\n
        UserResponse: User data
    """
    logger.info(f"Create user {user.email}")

    user_controller = UserController(user)

    user_controller.create_user()

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder(
            UserResponse(user.dict())
        )  
    )