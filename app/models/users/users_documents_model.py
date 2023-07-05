from typing import Optional

from models.globals_model import TimeStampModel
from models.enums import DocumentTypeEnum


class Documents(TimeStampModel):
    """
    Model for documents
    Args:
        TimeStampModel (Model): The global model insert timestamp on model
    """
    user_id: Optional[str]
    document_type: DocumentTypeEnum
    document_number: str
