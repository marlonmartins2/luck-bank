from typing import Optional

from pydantic import BaseModel

from models.globals_model import TimeStampModel


class Address(TimeStampModel):
    """
    Model for address
    Args:
        TimeStampModel (Model): The global model insert timestamp on model
    """

    class Config:
        """
        Config for address
        Args:
            Config (Config): The global config for this model.
        """
        anystr_strip_whitespace = True
        anystr_lower = True

    user_id: str
    street: str
    number: str
    complement: Optional[str]
    neighborhood: str
    city: str
    state: str
    country: str
    zip_code: str


class AddressCreateRequest(BaseModel):
    """
    Model for address create from request
    Args:
        BaseModel (Pydantic): The Pydantic base model.
    """
    user_id: str
    street: str
    number: str
    complement: Optional[str]
    neighborhood: str
    city: str
    state: str
    country: str
    zip_code: str
