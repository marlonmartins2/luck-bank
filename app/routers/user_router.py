from utils.logger import Logger

from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from models.users.users_model import UserUpdateRequest
from models.users.users_address_model import AddressCreateRequest, AddressUpdateRequest
from models.users.users_bank_account_model import BankAccountCreateRequest

from services.oauth2 import require_user, AuthJWT

from database.controllers.user import (
    get_user_by_id,
    user_detail,
    update_user_model,
    delete_user_by_id,
)

from database.controllers.address import (
    create_address,
    get_address_per_user,
    get_address_by_id,
    update_address,
    delete_address,

)

from database.controllers.account import (
    create_account,
    get_accounts_per_user,
    get_account_by_id,
    update_account_type,
    delete_account,
)


logger = Logger.init("UserRouteLogger")


user_router = APIRouter(tags=["User"], dependencies=[Depends(require_user), ])


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


@user_router.get("/users/{user_id}/address/", status_code=status.HTTP_200_OK)
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


@user_router.get("/users/{user_id}/address/{address_id}/", status_code=status.HTTP_200_OK)
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


@user_router.post("/users/{user_id}/address/", status_code=status.HTTP_201_CREATED)
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


@user_router.patch("/users/{user_id}/address/{address_id}/", status_code=status.HTTP_200_OK)
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


@user_router.delete("/users/{user_id}/address/{address_id}/", status_code=status.HTTP_200_OK)
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


@user_router.get("/users/{user_id}/accounts/", status_code=status.HTTP_200_OK)
def get_user_accounts(user_id: str):
    """
    Get user accounts endpoint:

    Returns:
    - **AccountResponse** (Account): Account data to database return.
    """
    logger.info(f"Get user accounts")

    accounts = get_accounts_per_user(user_id)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(accounts)
    )


@user_router.get("/users/{user_id}/accounts/{account_id}/", status_code=status.HTTP_200_OK)
def get_user_account_detail(user_id: str, account_id: str):
    """
    Get user account detail endpoint:

    Returns:
    - **AccountResponse** (Account): Account data to database return.
    """
    logger.info(f"Get user account detail")

    account = get_account_by_id(user_id, account_id)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(account)
    )


@user_router.post("/users/{user_id}/accounts/", status_code=status.HTTP_201_CREATED)
def create_user_account(user_id: str, payload: BankAccountCreateRequest):
    """
    Create user account endpoint:

    - **user_id**: the user id(str)
    - **payload**: the user payload to create(BankAccountCreateRequest)
    
    Returns:
    - **AccountResponse** (Account): Account data to database return.
    """
    logger.info(f"Create user account")

    new_account = create_account(user_id, payload)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "User account created successfully.",
            "payload": jsonable_encoder(new_account),
        }
    )


@user_router.patch("/users/{user_id}/accounts/{account_id}/", status_code=status.HTTP_200_OK)
def update_user_account(user_id: str, account_id: str, payload: BankAccountCreateRequest):
    """
    Update user account endpoint:

    - **user_id**: the user id(str)
    - **payload**: the user payload to update(BankAccountCreateRequest)
    
    Returns:
    - **AccountResponse** (Account): Account data to database return.
    """
    logger.info(f"Update user account")

    updated_account = update_account_type(user_id, account_id, payload)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "User account updated successfully.",
            "payload": jsonable_encoder(updated_account),
        }
    )


@user_router.delete("/users/{user_id}/accounts/{account_id}/", status_code=status.HTTP_200_OK)
def delete_user_account(user_id: str, account_id: str):
    """
    Delete user account endpoint:

    - **user_id**: the user id(str)
    
    Returns:
    - Message to user account deleted successfully.
    """
    logger.info(f"Delete user account")

    delete_account(account_id, user_id)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "User account deleted successfully.",}
    )
