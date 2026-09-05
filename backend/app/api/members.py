import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.permissions import (
    PERMISSION_MEMBERS_CREATE,
    PERMISSION_MEMBERS_DELETE,
    PERMISSION_MEMBERS_READ,
    PERMISSION_MEMBERS_UPDATE,
    require_permission,
)
from app.models.membership import Membership
from app.schemas.member import MemberInvite, MemberResponse, MemberRoleUpdate
from app.services.member_service import (
    invite_member,
    list_members,
    remove_member,
    update_member_role,
)

router = APIRouter(prefix="/organizations/{org_id}/members", tags=["members"])


@router.get("", response_model=list[MemberResponse])
async def get_members(
    org_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _: Membership = Depends(require_permission(PERMISSION_MEMBERS_READ)),
):
    return await list_members(db, org_id)


@router.post("", response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
async def add_member(
    org_id: uuid.UUID,
    data: MemberInvite,
    db: AsyncSession = Depends(get_db),
    actor: Membership = Depends(require_permission(PERMISSION_MEMBERS_CREATE)),
):
    try:
        return await invite_member(db, org_id, data.email, data.role_name)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{target_user_id}", response_model=MemberResponse)
async def change_member_role(
    org_id: uuid.UUID,
    target_user_id: uuid.UUID,
    data: MemberRoleUpdate,
    db: AsyncSession = Depends(get_db),
    actor: Membership = Depends(require_permission(PERMISSION_MEMBERS_UPDATE)),
):
    try:
        return await update_member_role(db, org_id, target_user_id, data.role_name, actor)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.delete("/{target_user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_member(
    org_id: uuid.UUID,
    target_user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    actor: Membership = Depends(require_permission(PERMISSION_MEMBERS_DELETE)),
):
    try:
        await remove_member(db, org_id, target_user_id, actor)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    return None
