from fastapi import status, APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from utils.logger import Logger

from services.oauth2 import require_user, AuthJWT

from models.users.users_address_model import AddressCreateRequest, AddressUpdateRequest

from database.controllers.address import (
    create_address,
    get_address_per_user,
    get_address_by_id,
    update_address,
    delete_address,
)


logger = Logger.init("AddressRouteLogger")

address_router = APIRouter(tags=["Address"], dependencies=[Depends(require_user)])


@address_router.get("/users/{user_id}/address/", status_code=status.HTTP_200_OK)
def get_user_address(user_id: str):
    """
    Get user address endpoint:

    Returns:
    - **UserResponse** (User): User data to database return.
    """
    logger.info(f"Get user address")

    address = get_address_per_user(user_id)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(address)
    )


@address_router.get("/users/{user_id}/address/{address_id}/", status_code=status.HTTP_200_OK)
def get_user_address_detail(user_id: str, address_id: str):
    """
    Get user address detail endpoint:

    Returns:
    - **AddressResponse** (Address): Address data to database return.
    """
    logger.info(f"Get user address detail")

    address = get_address_by_id(user_id, address_id)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(address)
    )


@address_router.post("/users/{user_id}/address/", status_code=status.HTTP_201_CREATED)
def create_user_address(user_id: str, payload: AddressCreateRequest):
    """
    Create user address endpoint:

    - **user_id**: the user id(str)
    - **payload**: the user payload to create(AddressCreateRequest)
    
    Returns:
    - **AddresResponse** (Address): Address data to database return.
    """
    logger.info(f"Create user address")

    new_address = create_address(user_id, payload)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "User address created successfully.",
            "payload": jsonable_encoder(new_address),
        }
    )


@address_router.patch("/users/{user_id}/address/{address_id}/", status_code=status.HTTP_200_OK)
def update_user_address(user_id: str, address_id: str, payload: AddressUpdateRequest):
    """
    Update user address endpoint:

    - **user_id**: the user id(str)
    - **payload**: the user payload to update(AddressUpdateRequest)
    
    Returns:
    - **AddresResponse** (Address): Address data to database return.
    """
    logger.info(f"Update user address")

    updated_address = update_address(user_id, address_id, payload)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "User address updated successfully.",
            "payload": jsonable_encoder(updated_address),
        }
    )


@address_router.delete("/users/{user_id}/address/{address_id}/", status_code=status.HTTP_200_OK)
def delete_user_address(user_id: str, address_id: str):
    """
    Delete user address endpoint:

    - **user_id**: the user id(str)
    
    Returns:
    - Message to user address deleted successfully.
    """
    logger.info(f"Delete user address")

    delete_address(address_id, user_id)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "User address deleted successfully.",}
    )
