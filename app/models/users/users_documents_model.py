from typing import Optional

from pydantic import BaseModel

from models.globals_model import TimeStampModel
from models.enums import DocumentTypeEnum


class Documents(TimeStampModel):
    """
    Model for documents
    Args:
        TimeStampModel (Model): The global model insert timestamp on model
    """
    user_id: str
    document_type: DocumentTypeEnum
    document_number: str


class DocumentsCreateRequest(BaseModel):
    """
    Model for documents create from request
    Args:
        BaseModel (Pydantic): The Pydantic base model.
    """
    user_id: str
    document_type: DocumentTypeEnum
    document_number: str
