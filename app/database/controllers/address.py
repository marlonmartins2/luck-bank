from datetime import datetime

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

from pymongo.errors import (
    ServerSelectionTimeoutError,
    ConnectionFailure,
    OperationFailure,
    PyMongoError
)

from utils.logger import Logger

from database import database, Collections

from models.users.users_address_model import Address


logger = Logger.init("AddressControllerLogger")


def create_address(user_id, address):
    """
    Create address from user create request.
    Args:
        user_id (str): The user id.
        address (Address): The address data.
    """
    logger.info(f"Create address from user_id: ->: {user_id}")
    try:

        address_has_exist = database[Collections.USER_ADDRESSES].find_one(
            {
                "user_id": user_id,
                "street": address.street,
                "number": address.number,
                "zip_code": address.zip_code,
            },
            {"_id": 0}
        )
        if address_has_exist and address_has_exist["deleted_at"] == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "Address already exists",
                    "address": jsonable_encoder(address_has_exist),
                }
            )

        elif address_has_exist and address_has_exist["deleted_at"] != "":
            database[Collections.USER_ADDRESSES].update_one(
                {"id": address_has_exist["id"]},
                {
                    "$set": {
                        "deleted_at": "",
                        "updated_at": datetime.now()
                    }
                }
            )

            return address_has_exist

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

        address.pop("_id")

        return address

    except ServerSelectionTimeoutError as error:
        logger.debug(f"ServerSelectionTimeoutError: {error}")

    except ConnectionFailure as error:
        logger.debug(f"ConnectionFailure: {error}")

    except OperationFailure as error:
        logger.debug(f"OperationFailure: {error}")

    except PyMongoError as error:
        logger.debug(f"PyMongoError: {error}")


def get_address_per_user(user_id):
    """
    Get address per user.
    Args:
        user_id (str): The user id.
    """
    logger.info(f"Get address per user_id: ->: {user_id}")
    payload = []

    try:
        addresses = database[Collections.USER_ADDRESSES].find(
            {"user_id": user_id, "deleted_at": ""},
            {"_id": 0}
        )

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


def get_address_by_id(user_id , address_id):
    """
    Get address by id.
    Args:
        address_id (str): The address id.
    """
    logger.info(f"Get address detail user id: ->: {user_id}")

    try:
        address = database[Collections.USER_ADDRESSES].find_one(
            {"id": address_id, "user_id": user_id},
            {"_id": 0}
        )

        return address

    except ServerSelectionTimeoutError as error:
        logger.debug(f"ServerSelectionTimeoutError: {error}")

    except ConnectionFailure as error:
        logger.debug(f"ConnectionFailure: {error}")

    except OperationFailure as error:
        logger.debug(f"OperationFailure: {error}")

    except PyMongoError as error:
        logger.debug(f"PyMongoError: {error}")


def update_address(user_id, address_id, payload):
    """
    Update address per user.
    Args:
        user_id (str): The user id.
        address (Address): The address data.
    """
    logger.info(f"Update address per user_id: ->: {user_id}")

    try:
        address = payload.dict(exclude_none=True)
        address["updated_at"] = datetime.now()

        database[Collections.USER_ADDRESSES].update_one(
            {"id": address_id},
            {"$set": address}
        )

        address = database[Collections.USER_ADDRESSES].find_one(
            {"id": address_id},
            {"_id": 0}
        )

        return address

    except ServerSelectionTimeoutError as error:
        logger.debug(f"ServerSelectionTimeoutError: {error}")

    except ConnectionFailure as error:
        logger.debug(f"ConnectionFailure: {error}")

    except OperationFailure as error:
        logger.debug(f"OperationFailure: {error}")

    except PyMongoError as error:
        logger.debug(f"PyMongoError: {error}")


def delete_address(address_id, user_id):
    """
    Delete address per user.
    Args:
        address_id (str): The address id.
    """
    logger.info(f"Delete address per user id: ->: {user_id}")

    try:
        database[Collections.USER_ADDRESSES].update_one(
            {"id": address_id},
            {"$set": {"deleted_at": datetime.now()}}
        )

        return True

    except ServerSelectionTimeoutError as error:
        logger.debug(f"ServerSelectionTimeoutError: {error}")

    except ConnectionFailure as error:
        logger.debug(f"ConnectionFailure: {error}")

    except OperationFailure as error:
        logger.debug(f"OperationFailure: {error}")

    except PyMongoError as error:
        logger.debug(f"PyMongoError: {error}")
