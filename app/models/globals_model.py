from uuid import uuid4

from pydantic import BaseModel

from typing import Optional

from datetime import datetime


class TimeStampModel(BaseModel):
    """
    Model for timestamp
    Args:
        BaseModel (Model): Model for timestamp
    """
    id: str = str(uuid4())
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    deleted_at: datetime = ""