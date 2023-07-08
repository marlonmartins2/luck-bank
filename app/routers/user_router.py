from utils.logger import Logger

from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from models.users.users_model import UserUpdateRequest
from models.users.users_address_model import AddressCreateRequest, AddressUpdateRequest

from services.oauth2 import require_user, AuthJWT

from database.controllers.user import (
    get_user_by_id,
    user_detail,
    update_user_model,
    delete_user_by_id,
)


logger = Logger.init("UserRouteLogger")

user_router = APIRouter(tags=["User"], dependencies=[Depends(require_user)])


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

    updated_user = update_user_model(user_id, payload)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "User updated successfully.",
            "payload": jsonable_encoder(updated_user),
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
