from uuid import uuid4

from random import randint

from datetime import datetime

from models.enums import StatusEnum, AccountTypeEnum

from models.globals_model import TimeStampModel


class BankAccount(TimeStampModel):
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
    agency: int = "0001"
    agency_digit: int = 0
    status: StatusEnum = StatusEnum.PENDING


class BankAccountCreateRequest(TimeStampModel):
    """
    Model for user bank account create from request
    Args:
        TimeStampModel (Model): The global model insert timestamp on model
    """
    account_type: AccountTypeEnum
