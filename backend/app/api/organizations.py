import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.organization import Organization
from app.models.role import Role
from app.models.user import User
from app.schemas.organization import (
    MembershipResponse,
    OrganizationCreate,
    OrganizationResponse,
    OrganizationUpdate,
)
from app.services.organization_service import (
    OWNER_ROLE_NAME,
    create_organization,
    delete_organization,
    get_membership,
    get_organization,
    get_user_organizations,
    update_organization,
)

router = APIRouter(prefix="/organizations", tags=["organizations"])


@router.post("", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_org(
    data: OrganizationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        organization = await create_organization(db, current_user.id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return organization


@router.get("", response_model=list[OrganizationResponse])
async def list_orgs(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    organizations = await get_user_organizations(db, current_user.id)
    return organizations


async def _get_membership_or_404(
    db: AsyncSession, user_id: uuid.UUID, org_id: uuid.UUID
) -> "Membership":
    membership = await get_membership(db, user_id, org_id)
    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this organization",
        )
    return membership


@router.get("/{org_id}", response_model=OrganizationResponse)
async def get_org(
    org_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    organization = await get_organization(db, org_id)
    if organization is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    await _get_membership_or_404(db, current_user.id, org_id)
    return organization


@router.patch("/{org_id}", response_model=OrganizationResponse)
async def patch_org(
    org_id: uuid.UUID,
    data: OrganizationUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    organization = await get_organization(db, org_id)
    if organization is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    await _get_membership_or_404(db, current_user.id, org_id)
    return await update_organization(db, organization, data)


@router.delete("/{org_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_org(
    org_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    organization = await get_organization(db, org_id)
    if organization is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")

    membership = await _get_membership_or_404(db, current_user.id, org_id)
    role = await db.get(Role, membership.role_id)
    if role is None or role.name != OWNER_ROLE_NAME:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the OWNER can delete an organization",
        )

    await delete_organization(db, organization)
    return None
