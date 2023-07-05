from utils.logger import Logger

from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from models.users.users_model import UserCreateRequest

from database.controllers.user import create_user_model
from database.controllers.user import get_user_by_id


logger = Logger.init("UserRouteLogger")


user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.post("/users/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreateRequest):
    """
    Create user endpoint:

    - **first_name**: the user first name(str)
    - **last_name**: the user last name(str)
    - **email**: the user email(valid email str)
    - **password**: the user password(str > 8 length)
    - **confirm_password**: the user password confirmation(str > 8 length)
    - **phone**: the user phone(str)
    - **documents**: the user documents(list)
    - **address**: the user address(list)
    - **accounts**: the user accounts(list)

    Returns:
    - **UserResponse** (User): User data to be created.
    - **AccountResponse** (UserBankAccount): User bank account data to be created.
    """
    logger.info(f"Create user {user.email}")

    create_user_model(user)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content="Please check your email to confirm your account."
    )


@user_router.get("/users/{user_id}/", status_code=status.HTTP_200_OK)
def get_user(user_id: str):
    """
    Get user endpoint:

    - **user_id**: the user id(str)

    Returns:
    - **UserResponse** (User): User data to database return.
    """
    logger.info(f"Get user {user_id}")

    user = get_user_by_id(user_id)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(user)
    )
