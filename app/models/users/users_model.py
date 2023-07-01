from uuid import uuid4

from random import randint

from datetime import datetime, date

from pydantic import BaseModel, SecretStr, EmailStr

from typing import Optional, List, Dict

from models.users import DocumentTypeEnum, StatusEnum, AccountTypeEnum


class Documents(BaseModel):
    """
    Model for documents
    Args:
        BaseModel (Model): Model for documents
    """
    document_type: DocumentTypeEnum
    document_number: str


class Address(BaseModel):
    """
    Model for address
    Args:
        BaseModel (Model): Model for address
    """
    street: str
    number: str
    complement: Optional[str]
    neighborhood: str
    city: str
    state: str
    country: str
    zip_code: str


class UserBankAccount(BaseModel):
    """
    Model for user bank account
    Args:
        BaseModel (Model): Model for user bank account
    """
    id: str = str(uuid4())
    user_id: str
    account_type: AccountTypeEnum
    account_number: int = randint(100000, 999999)
    account_digit: int = randint(0, 9)
    agency: int = randint(1000, 9999)
    agency_digit: int = randint(0, 9)
    status: StatusEnum = StatusEnum.PENDING
    created_at: datetime = datetime.now()
    updated_at: datetime = ""
    deleted_at: datetime = ""


class UserBankAccountCreateRequest(BaseModel):
    """
    Model for user bank account create from request
    Args:
        BaseModel (Model): Model for user bank account create from request
    """
    account_type: AccountTypeEnum


class User(BaseModel):
    """
    Model for user
    Args:
        BaseModel (Model): Model for user
    """
    id: str = str(uuid4())
    first_name: str
    last_name: str
    email: EmailStr
    password: SecretStr
    phone: str
    address: Address
    status: StatusEnum = StatusEnum.PENDING
    is_active: bool = False
    last_login: datetime = ""
    created_at: datetime = datetime.now()
    updated_at: datetime = ""
    deleted_at: datetime = ""


class UserCreateRequest(BaseModel):
    """
    Model for user create from request
    Args:
        BaseModel (Model): Model for user create from request
    """
    first_name: str
    last_name: str
    email: EmailStr
    password: SecretStr
    confirm_password: SecretStr
    phone: str
    documents: List[Documents]
    address: List[Address]
    account: List[UserBankAccountCreateRequest]


class UserResponse(BaseModel):
    """
    Model for user return in response
    Args:
        BaseModel (Model): Model for user return in response
    """
    id: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    documents: List[Documents]
    address: Address
    status: StatusEnum
    is_active: bool
    account: List[UserBankAccount]
    last_login: datetime
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime
