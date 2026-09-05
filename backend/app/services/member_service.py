import uuid

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.permissions import ROLE_ADMIN, ROLE_OWNER, get_role_by_name
from app.models.membership import Membership
from app.models.role import Role
from app.models.user import User
from app.schemas.member import MemberResponse


async def list_members(db: AsyncSession, org_id: uuid.UUID) -> list[MemberResponse]:
    result = await db.execute(
        select(Membership, User, Role)
        .join(User, User.id == Membership.user_id)
        .join(Role, Role.id == Membership.role_id)
        .where(Membership.organization_id == org_id)
        .order_by(Membership.created_at)
    )
    return [
        MemberResponse(
            user_id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            role=role.name,
            role_id=role.id,
            created_at=membership.created_at,
        )
        for membership, user, role in result.all()
    ]


async def get_member(db: AsyncSession, org_id: uuid.UUID, user_id: uuid.UUID) -> Membership | None:
    result = await db.execute(
        select(Membership).where(
            Membership.organization_id == org_id,
            Membership.user_id == user_id,
        )
    )
    return result.scalar_one_or_none()


async def invite_member(
    db: AsyncSession, org_id: uuid.UUID, email: str, role_name: str
) -> MemberResponse:
    role = await get_role_by_name(db, role_name)
    if role is None:
        raise ValueError(f"Unknown role: {role_name}")

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if user is None or not user.is_active:
        raise ValueError("User is not registered with SupportAI")

    existing = await get_member(db, org_id, user.id)
    if existing is not None:
        raise ValueError("User is already a member of this organization")

    membership = Membership(user_id=user.id, organization_id=org_id, role_id=role.id)
    db.add(membership)
    await db.flush()

    response = MemberResponse(
        user_id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        role=role.name,
        role_id=role.id,
        created_at=membership.created_at,
    )
    return response


async def update_member_role(
    db: AsyncSession,
    org_id: uuid.UUID,
    target_user_id: uuid.UUID,
    role_name: str,
    actor_membership: Membership,
) -> MemberResponse:
    role = await get_role_by_name(db, role_name)
    if role is None:
        raise ValueError(f"Unknown role: {role_name}")

    target = await get_member(db, org_id, target_user_id)
    if target is None:
        raise ValueError("Member not found in this organization")

    actor_role = await db.get(Role, actor_membership.role_id)
    target_role = await db.get(Role, target.role_id)
    actor_is_owner = actor_role is not None and actor_role.name == ROLE_OWNER

    if target_role is not None and target_role.name == ROLE_OWNER and not actor_is_owner:
        raise PermissionError("Only the OWNER can manage the OWNER role")

    if target_user_id == actor_membership.user_id and role.name != ROLE_OWNER:
        raise ValueError("A member cannot demote themselves")

    target.role_id = role.id
    await db.flush()

    user = await db.get(User, target_user_id)
    assert user is not None

    return MemberResponse(
        user_id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        role=role.name,
        role_id=role.id,
        created_at=target.created_at,
    )


async def remove_member(
    db: AsyncSession,
    org_id: uuid.UUID,
    target_user_id: uuid.UUID,
    actor_membership: Membership,
) -> None:
    target = await get_member(db, org_id, target_user_id)
    if target is None:
        raise ValueError("Member not found in this organization")

    target_role = await db.get(Role, target.role_id)
    actor_role = await db.get(Role, actor_membership.role_id)

    if target_role is not None and target_role.name == ROLE_OWNER:
        raise PermissionError("The OWNER cannot be removed from the organization")

    if (
        actor_role is not None
        and actor_role.name != ROLE_OWNER
        and target_user_id != actor_membership.user_id
        and target_role is not None
        and target_role.name == ROLE_ADMIN
    ):
        raise PermissionError("Only the OWNER can remove an ADMIN")

    if target_user_id == actor_membership.user_id:
        owner_count = await db.execute(
            select(Membership)
            .join(Role, Role.id == Membership.role_id)
            .where(
                Membership.organization_id == org_id,
                Role.name == ROLE_OWNER,
            )
        )
        if len(owner_count.scalars().all()) == 1:
            raise ValueError("The last OWNER cannot leave the organization")

    await db.execute(
        delete(Membership).where(
            Membership.organization_id == org_id,
            Membership.user_id == target_user_id,
        )
    )
    await db.flush()
