from utils.logger import Logger

from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from models.users.users_model import UserCreateRequest, UserUpdateRequest

from services.oauth2 import require_user, AuthJWT

from database.controllers.user import (
    create_user_model,
    get_user_by_id,
    user_detail,
    update_user_model,
    delete_user_by_id,
)


logger = Logger.init("UserRouteLogger")


user_router = APIRouter(tags=["User"], dependencies=[Depends(require_user), ])


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


@user_router.patch("/users/{user_id}/", status_code=status.HTTP_200_OK)
def update_user(user_id: str, payload: UserUpdateRequest):
    """
    Update user endpoint:

    - **user_id**: the user id(str)
    - **payload**: the user payload to update(UserUpdateRequest)
    
    Returns:
    - **UserResponse** (User): User data to database return.
    """
    logger.info(f"Update user {user_id}")

    update_user_model(user_id, payload)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "User updated successfully.",
            "payload": jsonable_encoder(payload),
        }
    )


@user_router.delete("/users/{user_id}/", status_code=status.HTTP_200_OK)
def delete_user(user_id: str):
    """
    Delete user endpoint:

    - **user_id**: the user id(str)
    
    Returns:
    - Message to user deleted successfully.
    """
    logger.info(f"Delete user {user_id}")

    delete_user_by_id(user_id)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "User deleted successfully.",}
    )


@user_router.get("/user_details/", status_code=status.HTTP_200_OK)
def get_user_details(Authorize: AuthJWT = Depends()):
    """
    Get user details endpoint:

    Returns:
    - **UserResponse** (User): User data to database return.
    """
    logger.info(f"Get user details")

    user_id = Authorize.get_jwt_subject()

    user = user_detail(user_id)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(user)
    )
