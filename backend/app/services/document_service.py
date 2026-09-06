import uuid

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.tenant import TenantContext
from app.models.document import Document, DocumentStatus
from app.services.storage_service import (
    StorageService,
    bucket_for_category,
)

DOCUMENT_CATEGORY = "documents"


async def create_document(
    db: AsyncSession,
    *,
    tenant: TenantContext,
    storage: StorageService,
    filename: str,
    content: bytes,
    content_type: str | None,
) -> Document:
    """Validate, store in MinIO, and record the document metadata.

    The file is uploaded to object storage first; only when the upload succeeds
    is a database record created with status UPLOADED. Invalid files raise
    ``FileValidationError`` before anything is persisted.
    """
    stored = storage.upload(
        tenant=tenant,
        category=DOCUMENT_CATEGORY,
        filename=filename,
        content=content,
        content_type=content_type,
    )

    document = Document(
        organization_id=tenant.organization_id,
        filename=filename,
        mime_type=stored.content_type or "application/octet-stream",
        storage_key=stored.storage_key,
        size=len(content),
        status=DocumentStatus.UPLOADED.value,
        error_message=None,
        created_by=tenant.user_id,
    )
    db.add(document)
    await db.flush()
    return document


async def list_documents(db: AsyncSession, org_id: uuid.UUID) -> list[Document]:
    result = await db.execute(
        select(Document)
        .where(Document.organization_id == org_id)
        .order_by(Document.created_at.desc())
    )
    return list(result.scalars().all())


async def get_document(
    db: AsyncSession, org_id: uuid.UUID, document_id: uuid.UUID
) -> Document | None:
    """Return a document only if it belongs to the given organization."""
    result = await db.execute(
        select(Document).where(
            Document.organization_id == org_id,
            Document.id == document_id,
        )
    )
    return result.scalar_one_or_none()


async def delete_document(
    db: AsyncSession,
    *,
    tenant: TenantContext,
    storage: StorageService,
    document: Document,
) -> None:
    """Remove the stored object and the document record.

    A missing object is tolerated (we still delete the record); a cross-tenant
    key raises ``StorageAccessError``.
    """
    try:
        storage.delete(
            tenant=tenant,
            bucket=bucket_for_category(DOCUMENT_CATEGORY),
            storage_key=document.storage_key,
        )
    except FileNotFoundError:
        pass
    await db.execute(delete(Document).where(Document.id == document.id))
    await db.flush()
