from uuid import uuid4

from random import randint

from datetime import datetime

from pydantic import EmailStr

from typing import Optional, List, Dict

from models.users import DocumentTypeEnum, StatusEnum, AccountTypeEnum

from models import TimeStampModel


class Documents(TimeStampModel):
    """
    Model for documents
    Args:
        TimeStampModel (Model): The global model insert timestamp on model
    """
    user_id: Optional[str]
    document_type: DocumentTypeEnum
    document_number: str


class Address(TimeStampModel):
    """
    Model for address
    Args:
        TimeStampModel (Model): The global model insert timestamp on model
    """
    user_id: Optional[str]
    street: str
    number: str
    complement: Optional[str]
    neighborhood: str
    city: str
    state: str
    country: str
    zip_code: str


class UserBankAccount(TimeStampModel):
    """
    Model for user bank account
    Args:
        TimeStampModel (Model): The global model insert timestamp on model
    """
    id: str = str(uuid4())
    user_id: str
    account_type: AccountTypeEnum
    account_number: int = randint(100000, 999999)
    account_digit: int = randint(0, 9)
    agency: int = '0001'
    agency_digit: int = 0
    status: StatusEnum = StatusEnum.PENDING


class UserBankAccountCreateRequest(TimeStampModel):
    """
    Model for user bank account create from request
    Args:
        TimeStampModel (Model): The global model insert timestamp on model
    """
    account_type: AccountTypeEnum


class User(TimeStampModel):
    """
    Model for user
    Args:
        TimeStampModel (Model): The global model insert timestamp on model
    """
    id: str = str(uuid4())
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    phone: str
    status: StatusEnum = StatusEnum.PENDING
    is_active: bool = False
    last_login: datetime = ""


class UserCreateRequest(TimeStampModel):
    """
    Model for user create from request
    Args:
        TimeStampModel (Model): The global model insert timestamp on model
    """
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    confirm_password: str
    phone: str
    documents: List[Documents]
    address: List[Address]
    accounts: List[UserBankAccountCreateRequest]
