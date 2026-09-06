import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.permissions import (
    PERMISSION_DOCUMENTS_CREATE,
    PERMISSION_DOCUMENTS_DELETE,
    PERMISSION_DOCUMENTS_READ,
    require_tenant,
)
from app.core.tenant import TenantContext
from app.schemas.document import DocumentResponse
from app.services.document_service import (
    create_document,
    delete_document,
    get_document,
    list_documents,
)
from app.services.storage_service import FileValidationError, get_storage_service

router = APIRouter(prefix="/organizations/{org_id}/documents", tags=["documents"])


@router.post("", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    org_id: uuid.UUID,
    file: UploadFile,
    db: AsyncSession = Depends(get_db),
    tenant: TenantContext = Depends(require_tenant(PERMISSION_DOCUMENTS_CREATE)),
):
    content = await file.read()
    try:
        document = await create_document(
            db,
            tenant=tenant,
            storage=get_storage_service(),
            filename=file.filename or "untitled",
            content=content,
            content_type=file.content_type,
        )
    except FileValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return document


@router.get("", response_model=list[DocumentResponse])
async def get_documents(
    org_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _: TenantContext = Depends(require_tenant(PERMISSION_DOCUMENTS_READ)),
):
    return await list_documents(db, org_id)


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document_detail(
    org_id: uuid.UUID,
    document_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _: TenantContext = Depends(require_tenant(PERMISSION_DOCUMENTS_READ)),
):
    document = await get_document(db, org_id, document_id)
    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    return document


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_document(
    org_id: uuid.UUID,
    document_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    tenant: TenantContext = Depends(require_tenant(PERMISSION_DOCUMENTS_DELETE)),
):
    document = await get_document(db, org_id, document_id)
    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    await delete_document(db, tenant=tenant, storage=get_storage_service(), document=document)
    return None
