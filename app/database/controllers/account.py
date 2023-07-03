import logging

from database import database, Collections

from models.users import UserBankAccount


logger = logging.getLogger("AccountControllerLogger")


def create_account(user_id, account):
    account = UserBankAccount(
        user_id=user_id,
        account_type=account.account_type
    ).dict(),

    database[Collections.USER_ACCOUNTS].insert_one(account)
