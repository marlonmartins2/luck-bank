from fastapi import status, APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from utils.logger import Logger

from services.oauth2 import require_user, AuthJWT

from models.users.users_bank_account_model import BankAccountCreateRequest

from database.controllers.account import (
    create_account,
    get_accounts_per_user,
    get_account_by_id,
    update_account_type,
    delete_account,
)

accounts_router = APIRouter(tags=["Account"], dependencies=[Depends(require_user)])

logger = Logger.init("AccountRouteLogger")


@accounts_router.get("/users/{user_id}/accounts/", status_code=status.HTTP_200_OK)
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


@accounts_router.get("/users/{user_id}/accounts/{account_id}/", status_code=status.HTTP_200_OK)
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


@accounts_router.post("/users/{user_id}/accounts/", status_code=status.HTTP_201_CREATED)
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


@accounts_router.patch("/users/{user_id}/accounts/{account_id}/", status_code=status.HTTP_200_OK)
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


@accounts_router.delete("/users/{user_id}/accounts/{account_id}/", status_code=status.HTTP_200_OK)
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
