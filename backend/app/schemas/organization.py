import uuid
from datetime import datetime

from pydantic import BaseModel, field_validator


class OrganizationCreate(BaseModel):
    name: str
    slug: str | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()

    @field_validator("slug")
    @classmethod
    def normalize_slug(cls, v: str | None) -> str | None:
        if v is None:
            return None
        v = v.strip().lower()
        if not v:
            raise ValueError("Slug cannot be empty")
        return v


class OrganizationUpdate(BaseModel):
    name: str | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip() if v is not None else None


class OrganizationResponse(BaseModel):
    id: uuid.UUID
    name: str
    slug: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class MembershipResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    organization_id: uuid.UUID
    role_id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}
