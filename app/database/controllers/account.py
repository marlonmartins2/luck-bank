from utils.logger import Logger

from database import database, Collections

from models.users.users_bank_account_model import BankAccount

from pymongo.errors import (
    ServerSelectionTimeoutError,
    ConnectionFailure,
    OperationFailure,
    PyMongoError
)

logger = Logger.init("AccountControllerLogger")


def create_account(user_id, account):
    """
    Create account from user create request.
    Args:
        user_id (str): The user id.
        account (UserBankAccount): The account data.
    """
    logger.info(f"Create account from user_id ->: {user_id}")
    account = BankAccount(
        user_id=user_id,
        account_type=account.account_type
    ).dict()

    database[Collections.USER_BANK_ACCOUNTS].insert_one(account)


def get_accounts_per_user(user_id):
    """
    Get accounts per user.
    Args:
        user_id (str): The user id.
    """
    logger.info(f"Get accounts per user_id ->: {user_id}")
    payload = []
    try:
        accounts = database[Collections.USER_BANK_ACCOUNTS].find({"user_id": user_id}, {"_id": 0})

        for account in accounts:
            payload.append(account)
        return payload
    except ServerSelectionTimeoutError as error:
        logger.debug(f"ServerSelectionTimeoutError: {error}")

    except ConnectionFailure as error:
        logger.debug(f"ConnectionFailure: {error}")

    except OperationFailure as error:
        logger.debug(f"OperationFailure: {error}")

    except PyMongoError as error:
        logger.debug(f"PyMongoError: {error}")
