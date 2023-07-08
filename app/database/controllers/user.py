from datetime import datetime

from utils.logger import Logger

from services import Password

from database import database, Collections
from database.controllers.address import create_address, get_address_per_user
from database.controllers.account import create_account, get_accounts_per_user
from database.controllers.document import create_document, get_documents_per_user

from pymongo.errors import (
    ServerSelectionTimeoutError,
    ConnectionFailure,
    OperationFailure,
    PyMongoError
)

logger = Logger.init("UserControllerLogger")


def create_user_model(user):
    from models.users.users_model import User
    """
    Create user
    Args:
        user (User): The user data.
    Returns:
        UserResponse: User data
    """
    logger.info(f"Create user ->: {user.email}")

    try:
        user_payload = User(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password=Password.get_password_hash(user.password),
            phone=user.phone,
        ).dict()

        for address in user.address:
            create_address(user_payload["id"], address)
        for document in user.documents:
            create_document(user_payload["id"], document)
        for account in user.accounts:
            create_account(user_payload["id"], account)

        database[Collections.USERS].insert_one(user_payload)

        return user

    except ValueError as error:
        logger.error(f"Error creating user: {error}")
        raise ValueError(error)

    except ServerSelectionTimeoutError as error:
        logger.debug(f"ServerSelectionTimeoutError: {error}")

    except ConnectionFailure as error:
        logger.debug(f"ConnectionFailure: {error}")

    except OperationFailure as error:
        logger.debug(f"OperationFailure: {error}")

    except PyMongoError as error:
        logger.debug(f"PyMongoError: {error}")


def check_user_by_email(email):
    """
    check email exists in database
    Args:
        email (str): The user email.
    """
    logger.info(f"Check user by email ->: {email}")
    user = database[Collections.USERS].find_one({"email": email}, {"_id": 0})

    if user:
        logger.error(f"User already exists: {email}")
        return user

    logger.info(f"User not exists: {email}")
    return False


def get_user_by_id(user_id):
    """
    Get user by id
    Args:
        user_id (str): The user id.
    """
    logger.info(f"Get user by id ->: {user_id}")
    response = None
    try:
        user = database[Collections.USERS].find_one({"id": user_id}, {"_id": 0, "password": 0})

        if not user:
            logger.error(f"User not found: {user_id}")
            raise ValueError("User not found")

        response = {
            "id": user["id"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "email": user["email"],
            "phone": user["phone"],
            "status": user["status"],
            "is_active": user["is_active"],
            "last_login": user["last_login"],
            "accounts": get_accounts_per_user(user["id"]),
            "documents": get_documents_per_user(user["id"]),
            "address": get_address_per_user(user["id"]),
            "created_at": user["created_at"],
            "updated_at": user["updated_at"],
            "deleted_at": user["deleted_at"],
        }

        return response

    except ServerSelectionTimeoutError as error:
        logger.debug(f"ServerSelectionTimeoutError: {error}")

    except ConnectionFailure as error:
        logger.debug(f"ConnectionFailure: {error}")

    except OperationFailure as error:
        logger.debug(f"OperationFailure: {error}")

    except PyMongoError as error:
        logger.debug(f"PyMongoError: {error}")


def update_user_model(user_id, user):
    """
    Update user by id
    Args:
        user_id (str): The user id.
        payload (dict): The user data.
    """
    logger.info(f"update user by id ->: {user_id}\npayload: {user}")
    try:
        payload = user.dict(exclude_none=True)
        payload["updated_at"] = datetime.now()
        
        database[Collections.USERS].update_one(
            {"id": user_id},
            {"$set": payload}
        )

        user = database[Collections.USERS].find_one({"id": user_id}, {"_id": 0, "password": 0})

        return user

    except ServerSelectionTimeoutError as error:
        logger.debug(f"ServerSelectionTimeoutError: {error}")
        return False

    except ConnectionFailure as error:
        logger.debug(f"ConnectionFailure: {error}")
        return False

    except OperationFailure as error:
        logger.debug(f"OperationFailure: {error}")
        return False

    except PyMongoError as error:
        logger.debug(f"PyMongoError: {error}")
        return False


def delete_user_by_id(user_id):
    """
    Delete user by id
    Args:
        user_id (str): The user id.
    """
    logger.info(f"delete user by id ->: {user_id}")
    try:
        user = database[Collections.USERS].find_one({"id": user_id}, {"_id": 0, "password": 0})
        
        if not user:
            logger.error(f"User not found: {user_id}")
            raise ValueError("User not found")
        
        database[Collections.USERS].update_one(
            {"id": user_id},
            {"$set": {"deleted_at": datetime.now()}}
        )

        return True

    except ServerSelectionTimeoutError as error:
        logger.debug(f"ServerSelectionTimeoutError: {error}")
        return False

    except ConnectionFailure as error:
        logger.debug(f"ConnectionFailure: {error}")
        return False

    except OperationFailure as error:
        logger.debug(f"OperationFailure: {error}")
        return False

    except PyMongoError as error:
        logger.debug(f"PyMongoError: {error}")
        return False


def user_detail(user_id):
    """
    Get user detail by id
    Args:
        user_id (str): The user id.
    """
    logger.info(f"get user detail by id ->: {user_id}")

    try:
        user = database[Collections.USERS].find_one({"id": user_id}, {"_id": 0, "password": 0})

        return {
            "id": user["id"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "email": user["email"],
            "phone": user["phone"],
            "status": user["status"],
            "is_active": user["is_active"],
            "last_login": user["last_login"],
            "created_at": user["created_at"],
            "updated_at": user["updated_at"],
        }

    except ServerSelectionTimeoutError as error:
        logger.debug(f"ServerSelectionTimeoutError: {error}")
        return False

    except ConnectionFailure as error:
        logger.debug(f"ConnectionFailure: {error}")
        return False

    except OperationFailure as error:
        logger.debug(f"OperationFailure: {error}")
        return False

    except PyMongoError as error:
        logger.debug(f"PyMongoError: {error}")
        return False


def set_last_login(user_id):
    """
    Set last login in user database
    Args:
        user_id (str): The user id.
    """
    logger.info(f"set user last login id ->: {user_id}")
    try:    
        database[Collections.USERS].update_one(
            {"id": user_id},
            {"$set": {"last_login": datetime.now()}}
        )

        return True

    except ServerSelectionTimeoutError as error:
        logger.debug(f"ServerSelectionTimeoutError: {error}")
        return False

    except ConnectionFailure as error:
        logger.debug(f"ConnectionFailure: {error}")
        return False

    except OperationFailure as error:
        logger.debug(f"OperationFailure: {error}")
        return False

    except PyMongoError as error:
        logger.debug(f"PyMongoError: {error}")
        return False
