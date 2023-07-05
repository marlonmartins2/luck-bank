import logging

from database import database, Collections

from models.users.users_address_model import Address


logger = logging.getLogger("AddressControllerLogger")


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
    ).dict(),

    database[Collections.USER_ADDRESSES].insert_one(address)


def get_address_per_user(user_id):
    address = database[Collections.USER_ADDRESSES].find({"user_id": user_id})

    return list(address)
