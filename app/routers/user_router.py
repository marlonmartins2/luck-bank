import logging

from fastapi import APIRouter, status, Depends, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from models.users import (
    User,
    UserCreateRequest,
)

from database.controllers.user import create_user as UserController


logger = logging.getLogger("UserLogger")


user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.post("/users/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreateRequest, background_tasks: BackgroundTasks):
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

    background_tasks.add_task(UserController, user)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content="Please check your email to confirm your account."
    )
