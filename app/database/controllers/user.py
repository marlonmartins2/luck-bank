import logging

from database import database, Collections

from pydantic import ValidationError, validator
from pydantic.error_wrappers import ErrorWrapper

from models.users import UserCreateRequest, User, UserBankAccount, Documents, Address

from settings import settings

from services import Password


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
                addresses.append(
                    Address(
                        user_id=user_payload["id"],
                        street=address.street,
                        number=address.number,
                        complement=address.complement,
                        neighborhood=address.neighborhood,
                        city=address.city,
                        state=address.state,
                        country=address.country,
                        zip_code=address.zip_code
                    ).dict(),
                )

            for document in user.documents:
                documents.append(
                    Documents(
                        user_id=user_payload["id"],
                        document_type=document.document_type,
                        document_number=document.document_number
                    ).dict(),
                )
            for account in user.accounts:
                accounts.append(
                    UserBankAccount(
                        user_id=user_payload["id"],
                        account_type=account.account_type
                    ).dict(),
                )

            database[Collections.USERS].insert_one(user_payload)
            database[Collections.USER_ADDRESSES].insert_many(addresses)
            database[Collections.USER_DOCUMENTS].insert_many(documents)
            database[Collections.USER_BANK_ACCOUNTS].insert_many(accounts)

            return user

    except ValidationError as error:
        logger.error(f"Error creating user: {error}")
        return None
