import logging

from database import database

from pydantic import ValidationError, validator
from pydantic.error_wrappers import ErrorWrapper

from settings import settings

from models.users import UserCreateRequest

logger = logging.getLogger("UserControllerLogger")

class UserController:
    def __init__(self, user):
        self.collection = "users"
        self.user = user

    @validator("user", always=True)
    def validation_user(self):
        """
        Validate user payload.
        Args:
            user (User): User data
        """
        logger.info(f"Validate user ->: {self.user.email}")

        errors = []
        password = self.user.password.get_secret_value()
        password_confirm = self.user.confirm_password.get_secret_value()

        if database[self.collection].find_one({"email": self.user.email}):
            raise ValidationError("User already exists")

        if len(password) < settings.MINIMUM_PASSWORD_LENGTH:
            errors.append(
                ErrorWrapper(
                    ValidationError(
                        f"Password must be at least {settings.MINIMUM_PASSWORD_LENGTH} characters"
                    ),
                    loc=("password"),
                )
            )

        elif password != password_confirm:
            errors.append(
                ErrorWrapper(
                    ValidationError("Passwords do not match"),
                    loc=("password_confirm"),
                )
            )

        if errors:
            raise ValidationError(errors, model=UserCreateRequest)
        return True

    def create_user(self):
        """
        Create user
        Returns:
            UserResponse: User data
        """
        logger.info(f"Create user ->: {self.user.email}")

        try:
            user_validate = self.validation_user()

            if user_validate:
                database[self.collection].insert_one(self.user.dict())
                return self.user

        except ValidationError as error:
            logger.error(f"Error creating user: {error}")
            return None
