import uuid
from datetime import datetime

from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    filename: str
    mime_type: str
    storage_key: str
    size: int
    status: str
    error_message: str | None
    created_by: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
