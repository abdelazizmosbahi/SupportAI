import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.permissions import (
    PERMISSION_ORGANIZATION_DELETE,
    PERMISSION_ORGANIZATION_READ,
    PERMISSION_ORGANIZATION_UPDATE,
    require_permission,
)
from app.core.security import get_current_user
from app.models.membership import Membership
from app.models.user import User
from app.schemas.organization import (
    OrganizationCreate,
    OrganizationResponse,
    OrganizationUpdate,
)
from app.services.organization_service import (
    create_organization,
    delete_organization,
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


@router.get("/{org_id}", response_model=OrganizationResponse)
async def get_org(
    org_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    _: Membership = Depends(require_permission(PERMISSION_ORGANIZATION_READ)),
):
    organization = await get_organization(db, org_id)
    if organization is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    return organization


@router.patch("/{org_id}", response_model=OrganizationResponse)
async def patch_org(
    org_id: uuid.UUID,
    data: OrganizationUpdate,
    db: AsyncSession = Depends(get_db),
    _: Membership = Depends(require_permission(PERMISSION_ORGANIZATION_UPDATE)),
):
    organization = await get_organization(db, org_id)
    if organization is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    return await update_organization(db, organization, data)


@router.delete("/{org_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_org(
    org_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _: Membership = Depends(require_permission(PERMISSION_ORGANIZATION_DELETE)),
):
    organization = await get_organization(db, org_id)
    if organization is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")

    await delete_organization(db, organization)
    return None
