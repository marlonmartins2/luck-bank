from typing import Optional

from models.globals_model import TimeStampModel


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
