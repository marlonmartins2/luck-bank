import logging

from database import database, Collections

from models.users.users_bank_account_model import BankAccount


logger = logging.getLogger("AccountControllerLogger")


def create_account(user_id, account):
    """
    Create account from user create request.
    Args:
        user_id (str): The user id.
        account (UserBankAccount): The account data.
    """
    logger.info(f"Create account from user_id ->: {user_id}")
    account = BankAccount(
        user_id=user_id,
        account_type=account.account_type
    ).dict()

    database[Collections.USER_BANK_ACCOUNTS].insert_one(account)


def get_accounts_per_user(user_id):
    accounts = database[Collections.USER_BANK_ACCOUNTS].find({"user_id": user_id})

    return list(accounts)
