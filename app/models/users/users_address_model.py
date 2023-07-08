from typing import Optional

from pydantic import BaseModel

from models.globals_model import TimeStampModel


class Address(TimeStampModel):
    """
    Model for address
    Args:
        TimeStampModel (Model): The global model insert timestamp on model
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


class AddressCreateRequest(BaseModel):
    """
    Model for address create from request
    Args:
        BaseModel (Pydantic): The Pydantic base model.
    """
    class Config:
        """
        Config for address
        Args:
            Config (Config): The global config for this model.
        """
        anystr_strip_whitespace = True
        anystr_lower = True

    street: str
    number: str
    complement: Optional[str]
    neighborhood: str
    city: str
    state: str
    country: str
    zip_code: str


class AddressUpdateRequest(BaseModel):
    """
    Model for address update from request
    Args:
        BaseModel (Pydantic): The Pydantic base model.
    """
    class Config:
        """
        Config for address
        Args:
            Config (Config): The global config for this model.
        """
        anystr_strip_whitespace = True
        anystr_lower = True

    street: Optional[str]
    number: Optional[str]
    complement: Optional[str]
    neighborhood: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    zip_code: Optional[str]