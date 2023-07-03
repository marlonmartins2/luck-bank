from enum import Enum


class Collections(str, Enum):
    """
    Enum for collections to be used in database
    Args:
        str (Enum): Enum for collections to be used in database
    """
    USERS = "users"
    USER_BANK_ACCOUNTS = "user_bank_accounts"
    USER_DOCUMENTS = "user_documents"
    USER_ADDRESSES = "user_addresses"