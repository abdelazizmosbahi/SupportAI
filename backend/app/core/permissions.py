import uuid
from functools import cache

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.core.tenant import resolve_tenant
from app.models.role import Role
from app.models.user import User

# Permission codes
PERMISSION_ORGANIZATION_READ = "organization.read"
PERMISSION_ORGANIZATION_UPDATE = "organization.update"
PERMISSION_ORGANIZATION_DELETE = "organization.delete"

PERMISSION_MEMBERS_READ = "members.read"
PERMISSION_MEMBERS_CREATE = "members.create"
PERMISSION_MEMBERS_UPDATE = "members.update"
PERMISSION_MEMBERS_DELETE = "members.delete"

PERMISSION_DOCUMENTS_READ = "documents.read"
PERMISSION_DOCUMENTS_CREATE = "documents.create"
PERMISSION_DOCUMENTS_DELETE = "documents.delete"

PERMISSION_CONVERSATIONS_READ = "conversations.read"
PERMISSION_CONVERSATIONS_CREATE = "conversations.create"
PERMISSION_CONVERSATIONS_ASSIGN = "conversations.assign"
PERMISSION_MESSAGES_READ = "messages.read"
PERMISSION_MESSAGES_CREATE = "messages.create"

PERMISSION_TICKETS_READ = "tickets.read"
PERMISSION_TICKETS_CREATE = "tickets.create"
PERMISSION_TICKETS_UPDATE = "tickets.update"

PERMISSION_EVALUATIONS_READ = "evaluations.read"
PERMISSION_ANALYTICS_READ = "analytics.read"
PERMISSION_AUDIT_READ = "audit.read"

# Role names
ROLE_OWNER = "OWNER"
ROLE_ADMIN = "ADMIN"
ROLE_AGENT = "AGENT"
ROLE_VIEWER = "VIEWER"
ROLE_NAMES = {ROLE_OWNER, ROLE_ADMIN, ROLE_AGENT, ROLE_VIEWER}

# All permission codes (used to define OWNER as full access)
ALL_PERMISSIONS = [
    PERMISSION_ORGANIZATION_READ,
    PERMISSION_ORGANIZATION_UPDATE,
    PERMISSION_ORGANIZATION_DELETE,
    PERMISSION_MEMBERS_READ,
    PERMISSION_MEMBERS_CREATE,
    PERMISSION_MEMBERS_UPDATE,
    PERMISSION_MEMBERS_DELETE,
    PERMISSION_DOCUMENTS_READ,
    PERMISSION_DOCUMENTS_CREATE,
    PERMISSION_DOCUMENTS_DELETE,
    PERMISSION_CONVERSATIONS_READ,
    PERMISSION_CONVERSATIONS_CREATE,
    PERMISSION_CONVERSATIONS_ASSIGN,
    PERMISSION_MESSAGES_READ,
    PERMISSION_MESSAGES_CREATE,
    PERMISSION_TICKETS_READ,
    PERMISSION_TICKETS_CREATE,
    PERMISSION_TICKETS_UPDATE,
    PERMISSION_EVALUATIONS_READ,
    PERMISSION_ANALYTICS_READ,
    PERMISSION_AUDIT_READ,
]


@cache
def role_permissions(role_name: str) -> set[str]:
    if role_name == ROLE_OWNER:
        return set(ALL_PERMISSIONS)
    if role_name == ROLE_ADMIN:
        return {
            PERMISSION_ORGANIZATION_READ,
            PERMISSION_ORGANIZATION_UPDATE,
            PERMISSION_MEMBERS_READ,
            PERMISSION_MEMBERS_CREATE,
            PERMISSION_MEMBERS_UPDATE,
            PERMISSION_MEMBERS_DELETE,
            PERMISSION_DOCUMENTS_READ,
            PERMISSION_DOCUMENTS_CREATE,
            PERMISSION_DOCUMENTS_DELETE,
            PERMISSION_CONVERSATIONS_READ,
            PERMISSION_CONVERSATIONS_CREATE,
            PERMISSION_CONVERSATIONS_ASSIGN,
            PERMISSION_MESSAGES_READ,
            PERMISSION_MESSAGES_CREATE,
            PERMISSION_TICKETS_READ,
            PERMISSION_TICKETS_CREATE,
            PERMISSION_TICKETS_UPDATE,
            PERMISSION_EVALUATIONS_READ,
            PERMISSION_ANALYTICS_READ,
            PERMISSION_AUDIT_READ,
        }
    if role_name == ROLE_AGENT:
        return {
            PERMISSION_CONVERSATIONS_READ,
            PERMISSION_CONVERSATIONS_CREATE,
            PERMISSION_CONVERSATIONS_ASSIGN,
            PERMISSION_MESSAGES_READ,
            PERMISSION_MESSAGES_CREATE,
            PERMISSION_TICKETS_READ,
            PERMISSION_TICKETS_CREATE,
            PERMISSION_TICKETS_UPDATE,
            PERMISSION_EVALUATIONS_READ,
        }
    if role_name == ROLE_VIEWER:
        return {
            PERMISSION_ORGANIZATION_READ,
            PERMISSION_MEMBERS_READ,
            PERMISSION_DOCUMENTS_READ,
            PERMISSION_CONVERSATIONS_READ,
            PERMISSION_MESSAGES_READ,
            PERMISSION_TICKETS_READ,
            PERMISSION_EVALUATIONS_READ,
            PERMISSION_ANALYTICS_READ,
        }
    return set()


ROLE_PERMISSIONS_MAP: dict[str, list[str]] = {
    ROLE_OWNER: ALL_PERMISSIONS,
    ROLE_ADMIN: sorted(
        {
            PERMISSION_ORGANIZATION_READ,
            PERMISSION_ORGANIZATION_UPDATE,
            PERMISSION_MEMBERS_READ,
            PERMISSION_MEMBERS_CREATE,
            PERMISSION_MEMBERS_UPDATE,
            PERMISSION_MEMBERS_DELETE,
            PERMISSION_DOCUMENTS_READ,
            PERMISSION_DOCUMENTS_CREATE,
            PERMISSION_DOCUMENTS_DELETE,
            PERMISSION_CONVERSATIONS_READ,
            PERMISSION_CONVERSATIONS_CREATE,
            PERMISSION_CONVERSATIONS_ASSIGN,
            PERMISSION_MESSAGES_READ,
            PERMISSION_MESSAGES_CREATE,
            PERMISSION_TICKETS_READ,
            PERMISSION_TICKETS_CREATE,
            PERMISSION_TICKETS_UPDATE,
            PERMISSION_EVALUATIONS_READ,
            PERMISSION_ANALYTICS_READ,
            PERMISSION_AUDIT_READ,
        }
    ),
    ROLE_AGENT: sorted(
        {
            PERMISSION_CONVERSATIONS_READ,
            PERMISSION_CONVERSATIONS_CREATE,
            PERMISSION_CONVERSATIONS_ASSIGN,
            PERMISSION_MESSAGES_READ,
            PERMISSION_MESSAGES_CREATE,
            PERMISSION_TICKETS_READ,
            PERMISSION_TICKETS_CREATE,
            PERMISSION_TICKETS_UPDATE,
            PERMISSION_EVALUATIONS_READ,
        }
    ),
    ROLE_VIEWER: sorted(
        {
            PERMISSION_ORGANIZATION_READ,
            PERMISSION_MEMBERS_READ,
            PERMISSION_DOCUMENTS_READ,
            PERMISSION_CONVERSATIONS_READ,
            PERMISSION_MESSAGES_READ,
            PERMISSION_TICKETS_READ,
            PERMISSION_EVALUATIONS_READ,
            PERMISSION_ANALYTICS_READ,
        }
    ),
}


async def get_role_by_name(db: AsyncSession, role_name: str) -> Role | None:
    result = await db.execute(select(Role).where(Role.name == role_name))
    return result.scalar_one_or_none()


async def ensure_roles_seeded(db: AsyncSession) -> None:
    for role_name, permissions in ROLE_PERMISSIONS_MAP.items():
        result = await db.execute(select(Role).where(Role.name == role_name))
        role = result.scalar_one_or_none()
        if role is None:
            db.add(Role(name=role_name, permissions=permissions))
    await db.flush()


def require_permission(permission: str):
    async def permission_checker(
        org_id: uuid.UUID,
        request: Request,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ):
        del request
        context = await resolve_tenant(db, current_user.id, org_id)
        if permission not in context.permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return context.membership

    return permission_checker
