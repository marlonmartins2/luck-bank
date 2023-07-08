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
    id: Optional[str]
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    deleted_at: datetime = ""

    def __init__(self, **data):
        """
        Define id if not exists.
        Args:
            data (dict): The data for model.
        """
        if "id" not in data:
            data["id"] = str(uuid4())
        super().__init__(**data)
