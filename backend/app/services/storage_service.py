"""File storage service backed by MinIO (S3-compatible object storage).

The service is the single place that talks to object storage. It owns:

- bucket management for the ``documents`` / ``avatars`` / ``exports`` buckets,
- file validation (extension, MIME type, size),
- unique, tenant-scoped storage keys,
- tenant enforcement on read/delete via the resolved ``TenantContext``.

Object keys always start with ``orgs/{organization_id}/`` so a tenant can only
ever read or delete objects that belong to it.
"""

from __future__ import annotations

import mimetypes
import uuid
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

from minio import Minio
from minio.error import S3Error

from app.core.config import settings
from app.core.tenant import TenantContext

# Categories we can store, mapped to the bucket setting that holds the bucket name.
CATEGORY_BUCKET_SETTING = {
    "documents": "MINIO_BUCKET_DOCUMENTS",
    "avatars": "MINIO_BUCKET_AVATARS",
    "exports": "MINIO_BUCKET_EXPORTS",
}

BUCKET_CATEGORIES = tuple(CATEGORY_BUCKET_SETTING)

# Extension -> accepted MIME types. A generic type (application/octet-stream or
# empty) is always accepted so browsers/clients that do not know the type are
# not rejected; anything else must match the extension.
EXTENSION_MIME_TYPES = {
    "pdf": ["application/pdf"],
    "txt": ["text/plain"],
    "docx": ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"],
}

GENERIC_CONTENT_TYPES = {None, "", "application/octet-stream"}

MAX_UPLOAD_SIZE_BYTES = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024


class FileValidationError(ValueError):
    """Raised when a file fails extension, MIME type, or size validation."""


class StorageAccessError(PermissionError):
    """Raised when a tenant tries to read or delete an object outside its scope."""


@dataclass(frozen=True)
class StoredFile:
    bucket: str
    storage_key: str
    content_type: str | None = None


def validate_file(filename: str, content_type: str | None, size_bytes: int) -> None:
    """Validate an uploaded file's extension, MIME type, and size.

    Raises ``FileValidationError`` when any check fails.
    """
    if size_bytes <= 0:
        raise FileValidationError("File is empty")

    ext = Path(filename or "").suffix.lower().lstrip(".")
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise FileValidationError(
            f"File type '{ext or '<none>'}' is not allowed. "
            f"Allowed: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )

    if size_bytes > MAX_UPLOAD_SIZE_BYTES:
        raise FileValidationError(
            f"File is too large: {size_bytes} bytes. Maximum is {settings.MAX_UPLOAD_SIZE_MB} MB"
        )

    if content_type not in GENERIC_CONTENT_TYPES:
        allowed = EXTENSION_MIME_TYPES.get(ext, [])
        if allowed and content_type not in allowed:
            raise FileValidationError(
                f"MIME type '{content_type}' does not match file type '.{ext}'"
            )


def bucket_for_category(category: str) -> str:
    if category not in CATEGORY_BUCKET_SETTING:
        raise FileValidationError(f"Unknown storage category '{category}'")
    return getattr(settings, CATEGORY_BUCKET_SETTING[category])


def generate_storage_key(org_id: uuid.UUID, category: str, filename: str) -> str:
    """Generate a unique, tenant-scoped storage key for an upload."""
    bucket_for_category(category)  # raises for unknown categories
    ext = Path(filename).suffix.lower()
    return f"orgs/{org_id}/{category}/{uuid.uuid4().hex}{ext}"


class StorageService:
    """MinIO-backed storage service for upload, download, and delete."""

    def __init__(self, client: Minio | None = None, bucket_names: list[str] | None = None):
        self.client = client or Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE,
        )
        self.bucket_names = bucket_names or [
            settings.MINIO_BUCKET_DOCUMENTS,
            settings.MINIO_BUCKET_AVATARS,
            settings.MINIO_BUCKET_EXPORTS,
        ]

    def ensure_buckets(self) -> None:
        """Create configured buckets if they do not exist (idempotent)."""
        for name in self.bucket_names:
            if not self.client.bucket_exists(name):
                self.client.make_bucket(name)

    def upload(
        self,
        *,
        tenant: TenantContext,
        category: str,
        filename: str,
        content: bytes,
        content_type: str | None,
    ) -> StoredFile:
        """Validate and upload file bytes, returning the stored object location."""
        validate_file(filename, content_type, len(content))

        bucket = bucket_for_category(category)
        storage_key = generate_storage_key(tenant.organization_id, category, filename)
        effective_content_type = (
            content_type
            or mimetypes.guess_type(filename)[0]
            or "application/octet-stream"
        )
        self.client.put_object(
            bucket,
            storage_key,
            BytesIO(content),
            length=len(content),
            content_type=effective_content_type,
        )
        return StoredFile(
            bucket=bucket,
            storage_key=storage_key,
            content_type=effective_content_type,
        )

    def download(self, *, tenant: TenantContext, bucket: str, storage_key: str) -> bytes:
        """Download an object's bytes, enforcing the tenant's key prefix."""
        self._authorize(tenant.organization_id, storage_key)
        try:
            response = self.client.get_object(bucket, storage_key)
        except S3Error as exc:
            raise FileNotFoundError(f"Object '{storage_key}' does not exist") from exc
        try:
            return response.read()
        finally:
            response.close()
            response.release_conn()

    def delete(self, *, tenant: TenantContext, bucket: str, storage_key: str) -> None:
        """Delete an object, enforcing the tenant's key prefix."""
        self._authorize(tenant.organization_id, storage_key)
        try:
            self.client.remove_object(bucket, storage_key)
        except S3Error as exc:
            raise FileNotFoundError(f"Object '{storage_key}' does not exist") from exc

    def _authorize(self, org_id: uuid.UUID, storage_key: str) -> None:
        prefix = f"orgs/{org_id}/"
        if not storage_key.startswith(prefix):
            raise StorageAccessError(
                f"Object '{storage_key}' does not belong to organization '{org_id}'"
            )


def get_storage_service() -> StorageService:
    """Return the process-wide storage service singleton."""
    global _storage_service
    if _storage_service is None:
        _storage_service = StorageService()
    return _storage_service


_storage_service: StorageService | None = None
