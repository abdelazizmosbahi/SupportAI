import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr


class MemberResponse(BaseModel):
    user_id: uuid.UUID
    email: str
    first_name: str | None
    last_name: str | None
    role: str
    role_id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}


class MemberInvite(BaseModel):
    email: EmailStr
    role_name: str


class MemberRoleUpdate(BaseModel):
    role_name: str
