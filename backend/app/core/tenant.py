"""Tenant isolation: resolve a user's membership + role within an organization.

Every organization-scoped endpoint must run membership resolution before touching
any tenant data. `resolve_tenant` is the single enforcement point; it raises 403
unless the user is a member of the requested organization.
"""

import uuid
from dataclasses import dataclass

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.membership import Membership
from app.models.role import Role
from app.models.user import User


@dataclass
class TenantContext:
    membership: Membership
    user_id: uuid.UUID
    organization_id: uuid.UUID
    role_id: uuid.UUID
    role_name: str | None
    permissions: set[str]


async def resolve_tenant(
    db: AsyncSession,
    user_id: uuid.UUID,
    org_id: uuid.UUID,
) -> TenantContext:
    """Return the tenant context for user+org, or 403 if the user is not a member.

    The membership query is always scoped by both ``user_id`` and ``org_id``,
    which is what makes cross-tenant access impossible: a user can only ever
    resolve a context for an organization they actually belong to.
    """
    result = await db.execute(
        select(Membership).where(
            Membership.user_id == user_id,
            Membership.organization_id == org_id,
        )
    )
    membership = result.scalar_one_or_none()
    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this organization",
        )

    role = await db.get(Role, membership.role_id)
    permissions = set(role.permissions) if role else set()

    return TenantContext(
        membership=membership,
        user_id=membership.user_id,
        organization_id=membership.organization_id,
        role_id=membership.role_id,
        role_name=role.name if role else None,
        permissions=permissions,
    )


async def get_tenant_context(
    org_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TenantContext:
    """FastAPI dependency that resolves the tenant context for the path org."""
    return await resolve_tenant(db, current_user.id, org_id)
