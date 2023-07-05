from utils.logger import Logger

from database import database, Collections

from models.users.users_address_model import Address

from pymongo.errors import (
    ServerSelectionTimeoutError,
    ConnectionFailure,
    OperationFailure,
    PyMongoError
)



logger = Logger.init("AddressControllerLogger")


def create_address(user_id, address):
    """
    Create address from user create request.
    Args:
        user_id (str): The user id.
        address (Address): The address data.
    """
    logger.info(f"Create address from user_id: ->: {user_id}")
    address = Address(
        user_id=user_id,
        street=address.street,
        number=address.number,
        complement=address.complement,
        neighborhood=address.neighborhood,
        city=address.city,
        state=address.state,
        country=address.country,
        zip_code=address.zip_code
    ).dict()

    database[Collections.USER_ADDRESSES].insert_one(address)


def get_address_per_user(user_id):
    """
    Get address per user.
    Args:
        user_id (str): The user id.
    """
    logger.info(f"Get address per user_id: ->: {user_id}")
    payload = []

    try:
        addresses = database[Collections.USER_ADDRESSES].find({"user_id": user_id}, {"_id": 0})

        for address in addresses:
            payload.append(address)
        return payload
    except ServerSelectionTimeoutError as error:
        logger.debug(f"ServerSelectionTimeoutError: {error}")

    except ConnectionFailure as error:
        logger.debug(f"ConnectionFailure: {error}")

    except OperationFailure as error:
        logger.debug(f"OperationFailure: {error}")

    except PyMongoError as error:
        logger.debug(f"PyMongoError: {error}")
