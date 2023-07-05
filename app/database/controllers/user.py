import logging


from services import Password

from database import database, Collections
from database.controllers.address import create_address
from database.controllers.account import create_account
from database.controllers.document import create_document


logger = logging.getLogger("UserControllerLogger")


def create_user(user):
    from models.users.users_model import User
    """
    Create user
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


def check_user_by_email(email):
    """
    check email exists in database
    Args:
        email (str): The user email.
    """
    logger.info(f"Check user by email ->: {email}")
    user_has_exist = database[Collections.USERS].find_one({"email": email})

    if user_has_exist:
        logger.error(f"User already exists: {email}")
        return True

    logger.info(f"User not exists: {email}")
    return False
