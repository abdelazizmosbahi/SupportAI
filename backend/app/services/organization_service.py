import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.permissions import ROLE_OWNER, ensure_roles_seeded, get_role_by_name
from app.models.membership import Membership
from app.models.organization import Organization
from app.models.role import Role
from app.schemas.organization import OrganizationCreate, OrganizationUpdate

OWNER_ROLE_NAME = ROLE_OWNER


async def get_or_create_owner_role(db: AsyncSession) -> Role:
    await ensure_roles_seeded(db)
    role = await get_role_by_name(db, OWNER_ROLE_NAME)
    assert role is not None
    return role


def slugify(value: str) -> str:
    value = value.strip().lower()
    return "-".join(value.split())


async def _ensure_unique_slug(db: AsyncSession, base_slug: str) -> str:
    candidate = base_slug
    counter = 1
    while True:
        result = await db.execute(select(Organization).where(Organization.slug == candidate))
        if result.scalar_one_or_none() is None:
            return candidate
        counter += 1
        candidate = f"{base_slug}-{counter}"


async def create_organization(
    db: AsyncSession, user_id: uuid.UUID, data: OrganizationCreate
) -> Organization:
    slug = data.slug or slugify(data.name)
    slug = await _ensure_unique_slug(db, slug)

    organization = Organization(name=data.name, slug=slug)
    db.add(organization)
    await db.flush()

    role = await get_or_create_owner_role(db)
    membership = Membership(
        user_id=user_id,
        organization_id=organization.id,
        role_id=role.id,
    )
    db.add(membership)
    await db.flush()

    await db.refresh(organization)
    return organization


async def get_user_organizations(db: AsyncSession, user_id: uuid.UUID) -> list[Organization]:
    result = await db.execute(
        select(Organization)
        .join(Membership, Membership.organization_id == Organization.id)
        .where(Membership.user_id == user_id)
        .order_by(Organization.created_at)
    )
    return list(result.scalars().all())


async def get_organization(db: AsyncSession, org_id: uuid.UUID) -> Organization | None:
    result = await db.execute(select(Organization).where(Organization.id == org_id))
    return result.scalar_one_or_none()


async def get_membership(
    db: AsyncSession, user_id: uuid.UUID, org_id: uuid.UUID
) -> Membership | None:
    result = await db.execute(
        select(Membership).where(
            Membership.user_id == user_id,
            Membership.organization_id == org_id,
        )
    )
    return result.scalar_one_or_none()


async def update_organization(
    db: AsyncSession, organization: Organization, data: OrganizationUpdate
) -> Organization:
    if data.name is not None:
        organization.name = data.name
    await db.flush()
    await db.refresh(organization)
    return organization


async def delete_organization(db: AsyncSession, organization: Organization) -> None:
    await db.execute(
        Membership.__table__.delete().where(Membership.organization_id == organization.id)
    )
    await db.delete(organization)
    await db.flush()
