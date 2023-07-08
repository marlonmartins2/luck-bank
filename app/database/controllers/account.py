from datetime import datetime

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

from pymongo.errors import (
    ServerSelectionTimeoutError,
    ConnectionFailure,
    OperationFailure,
    PyMongoError
)

from utils import AccountNotSalary
from utils.logger import Logger

from database import database, Collections

from models.users.users_bank_account_model import BankAccount

logger = Logger.init("AccountControllerLogger")


def create_account(user_id, account):
    """
    Create account from user create request.
    Args:
        user_id (str): The user id.
        account (UserBankAccount): The account data.
    """
    logger.info(f"Create account from user_id ->: {user_id}")
    try:
        account = BankAccount(
            user_id=user_id,
            account_type=account.account_type
        ).dict()

        database[Collections.USER_BANK_ACCOUNTS].insert_one(account)

        account.pop("_id")

        return account

    except ServerSelectionTimeoutError as error:
        logger.error(f"ServerSelectionTimeoutError: {error}")

    except ConnectionFailure as error:
        logger.error(f"ConnectionFailure: {error}")

    except OperationFailure as error:
        logger.error(f"OperationFailure: {error}")

    except PyMongoError as error:
        logger.error(f"PyMongoError: {error}")


def get_accounts_per_user(user_id):
    """
    Get accounts per user.
    Args:
        user_id (str): The user id.
    """
    logger.info(f"Get accounts per user_id ->: {user_id}")
    payload = []
    try:
        accounts = database[Collections.USER_BANK_ACCOUNTS].find(
            {"user_id": user_id, "deleted_at": ""},
            {"_id": 0}
        )

        for account in accounts:
            payload.append(account)
        return payload

    except ServerSelectionTimeoutError as error:
        logger.error(f"ServerSelectionTimeoutError: {error}")

    except ConnectionFailure as error:
        logger.error(f"ConnectionFailure: {error}")

    except OperationFailure as error:
        logger.error(f"OperationFailure: {error}")

    except PyMongoError as error:
        logger.error(f"PyMongoError: {error}")


def get_account_by_id(user_id , account_id):
    """
    Get account by id.
    Args:
        account_id (str): The account id.
    """
    logger.info(f"Get account detail user id: ->: {user_id}")

    try:
        account = database[Collections.USER_BANK_ACCOUNTS].find_one(
            {"id": account_id, "user_id": user_id},
            {"_id": 0}
        )

        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "message": "Account not found",
                }
            )

        return account

    except ServerSelectionTimeoutError as error:
        logger.error(f"ServerSelectionTimeoutError: {error}")

    except ConnectionFailure as error:
        logger.error(f"ConnectionFailure: {error}")

    except OperationFailure as error:
        logger.error(f"OperationFailure: {error}")

    except PyMongoError as error:
        logger.error(f"PyMongoError: {error}")


def update_account_type(user_id, account_id, payload):
    """
    Update account per user.
    Args:
        user_id (str): The user id.
        account (account): The account data.
    """
    logger.info(f"Update account per user_id: ->: {user_id}")

    try:

        account = database[Collections.USER_BANK_ACCOUNTS].find_one(
            {"id": account_id},
            {"_id": 0}
        )

        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "message": "Address not found",
                }
            )

        if account and account["account_type"] != "salary":
            raise AccountNotSalary("Account is not salary")

        account = payload.dict()
        account["updated_at"] = datetime.now()

        database[Collections.USER_BANK_ACCOUNTS].update_one(
            {"id": account_id},
            {"$set": account}
        )


        return account

    except AccountNotSalary:
        logger.error("Account is not salary")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Changing account type is only allowed for salary type accounts."
                    "Please create another account.",
            }
        )

    except ServerSelectionTimeoutError as error:
        logger.error(f"ServerSelectionTimeoutError: {error}")

    except ConnectionFailure as error:
        logger.error(f"ConnectionFailure: {error}")

    except OperationFailure as error:
        logger.error(f"OperationFailure: {error}")

    except PyMongoError as error:
        logger.error(f"PyMongoError: {error}")


def delete_account(account_id, user_id):
    """
    Delete account per user.
    Args:
        account_id (str): The account id.
    """
    logger.info(f"Delete account per user id: ->: {user_id}")

    try:
        database[Collections.USER_BANK_ACCOUNTS].update_one(
            {"id": account_id},
            {"$set": {"deleted_at": datetime.now()}}
        )

        return True

    except ServerSelectionTimeoutError as error:
        logger.error(f"ServerSelectionTimeoutError: {error}")

    except ConnectionFailure as error:
        logger.error(f"ConnectionFailure: {error}")

    except OperationFailure as error:
        logger.error(f"OperationFailure: {error}")

    except PyMongoError as error:
        logger.error(f"PyMongoError: {error}")
