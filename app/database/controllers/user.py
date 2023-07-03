import logging


from pydantic import ValidationError, validator
from pydantic.error_wrappers import ErrorWrapper

from models.users import UserCreateRequest, User

from settings import settings

from services import Password

from database import database, Collections
from database.controllers.address import create_address
from database.controllers.account import create_account
from database.controllers.document import create_document


logger = logging.getLogger("UserControllerLogger")


@validator("user", always=True)
def validation_user(user):
    """
    Validate user payload.
    Args:
        user (User): User data
    """
    logger.info(f"Validate user ->: {user.email}")

    errors = []

    if database[Collections.USERS].find_one({"email": user.email}):
        raise ValidationError("User already exists")

    if len(user.password) < settings.MINIMUM_PASSWORD_LENGTH:
        errors.append(
            ErrorWrapper(
                ValidationError(
                    f"Password must be at least {settings.MINIMUM_PASSWORD_LENGTH} characters"
                ),
                loc=("password"),
            )
        )

    elif user.password != user.password_confirm:
        errors.append(
            ErrorWrapper(
                ValidationError("Passwords do not match"),
                loc=("password_confirm"),
            )
        )

    if errors:
        raise ValidationError(errors, model=UserCreateRequest)

    return True


def create_user(user):
    """
    Create user
    Returns:
        UserResponse: User data
    """
    logger.info(f"Create user ->: {user.email}")

    addresses = []
    accounts = []
    documents = []

    try:
        user_validate = validation_user
        if user_validate:
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

    except ValidationError as error:
        logger.error(f"Error creating user: {error}")
        return None
