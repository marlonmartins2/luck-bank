import logging

from database import database, Collections

from models.users import Address


logger = logging.getLogger("AddressControllerLogger")


def create_address(user_id, address):
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
