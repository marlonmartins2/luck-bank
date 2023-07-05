from uuid import uuid4

from datetime import datetime

from typing import List

from pydantic import EmailStr, Field, validator, BaseModel

from models import TimeStampModel, StatusEnum

from models.users.users_address_model import AddressCreateRequest

from models.users.users_bank_account_model import BankAccountCreateRequest

from models.users.users_documents_model import DocumentsCreateRequest

from database.controllers.user import check_user_by_email


class User(TimeStampModel):
    """
    Model for user
    Args:
        TimeStampModel (Model): The global model insert timestamp on model
    """
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    phone: str
    status: StatusEnum = StatusEnum.PENDING
    is_active: bool = False
    last_login: datetime = ""


class UserCreateRequest(BaseModel):
    """
    Model for user create from request
    Args:
        BaseModel (Pydantic): the Pydantic base model.
    """
    class Config:
        """
        Config for user create from request
        Args:
            Config (Config): The global config for this model.
        """
        anystr_strip_whitespace = True

    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)
    phone: str = Field(...)
    documents: List[DocumentsCreateRequest]
    address: List[AddressCreateRequest]
    accounts: List[BankAccountCreateRequest]


    @validator("email")
    def email_has_exists(cls, email):
        """
        Validator for email exists in database.
        Args:
            email (str): The email from request
        Returns:
            email (str): The email from request
        """
        if check_user_by_email(email):
            raise ValueError("email already exists in database")
        return email


    @validator("confirm_password")
    def passwords_match(cls, confirm_password, values):
        """
        Validator for passwords match
        Args:
            confirm_password (str): The password confirmation
            values (dict): The values from request
        Returns:
            confirm_password (str): The password confirmation
        """
        if "password" in values and confirm_password != values["password"]:
            raise ValueError("passwords do not match")
        return confirm_password
