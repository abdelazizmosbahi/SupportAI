import uuid

import pytest
from minio.error import S3Error

from app.core.config import settings
from app.core.tenant import TenantContext
from app.models.membership import Membership
from app.services.storage_service import (
    FileValidationError,
    StorageAccessError,
    StorageService,
    StoredFile,
    bucket_for_category,
    generate_storage_key,
    get_storage_service,
    validate_file,
)


class FakeResponse:
    def __init__(self, data: bytes):
        self._data = data
        self.closed = False

    def read(self, *args, **kwargs):
        return self._data

    def close(self):
        self.closed = True

    def release_conn(self):
        pass


class FakeMinio:
    """In-memory MinIO stand-in storing (bucket, key) -> bytes."""

    def __init__(self):
        self.buckets: set[str] = set()
        self.objects: dict[tuple[str, str], bytes] = {}

    def bucket_exists(self, name: str) -> bool:
        return name in self.buckets

    def make_bucket(self, name: str) -> None:
        self.buckets.add(name)

    def put_object(self, bucket, key, data, length, content_type=None):
        self.objects[(bucket, key)] = data.read()

    def get_object(self, bucket, key):
        if (bucket, key) not in self.objects:
            raise S3Error(
                None,
                "NoSuchKey",
                "object does not exist",
                f"{bucket}/{key}",
                "req-id",
                "host-id",
            )
        return FakeResponse(self.objects[(bucket, key)])

    def remove_object(self, bucket, key):
        self.objects.pop((bucket, key), None)


def make_tenant(org_id: uuid.UUID | None = None) -> TenantContext:
    org_id = org_id or uuid.uuid4()
    membership = Membership(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        organization_id=org_id,
        role_id=uuid.uuid4(),
    )
    return TenantContext(
        membership=membership,
        user_id=membership.user_id,
        organization_id=org_id,
        role_id=membership.role_id,
        role_name="OWNER",
        permissions=set(),
    )


def make_service(client: FakeMinio | None = None) -> StorageService:
    client = client or FakeMinio()
    return StorageService(
        client=client,
        bucket_names=[
            settings.MINIO_BUCKET_DOCUMENTS,
            settings.MINIO_BUCKET_AVATARS,
            settings.MINIO_BUCKET_EXPORTS,
        ],
    )


class TestFileValidation:
    def test_rejects_empty_file(self):
        with pytest.raises(FileValidationError):
            validate_file("notes.pdf", "application/pdf", 0)

    def test_rejects_disallowed_extension(self):
        with pytest.raises(FileValidationError):
            validate_file("malware.exe", "application/octet-stream", 100)

    def test_rejects_oversize_file(self):
        too_big = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024 + 1
        with pytest.raises(FileValidationError):
            validate_file("big.pdf", "application/pdf", too_big)

    def test_rejects_mismatched_mime_type(self):
        with pytest.raises(FileValidationError):
            validate_file("notes.pdf", "text/html", 100)

    def test_accepts_matching_mime_type(self):
        validate_file("notes.pdf", "application/pdf", 100)

    def test_accepts_generic_octet_stream(self):
        validate_file("notes.pdf", "application/octet-stream", 100)

    def test_accepts_single_character_content_type(self):
        validate_file("notes.txt", "text/plain", 50)


class TestStorageKeyGeneration:
    def test_key_is_tenant_scoped_and_unique(self):
        org_id = uuid.uuid4()
        key = generate_storage_key(org_id, "documents", "report.PDF")
        assert key == f"orgs/{org_id}/documents/" + key.rsplit("/", 1)[1]
        assert key.startswith(f"orgs/{org_id}/documents/")
        assert key.endswith(".pdf")
        second = generate_storage_key(org_id, "documents", "report.PDF")
        assert second != key

    def test_unknown_category_raises(self):
        with pytest.raises(FileValidationError):
            generate_storage_key(uuid.uuid4(), "videos", "clip.mp4")

    def test_bucket_for_category_maps_to_settings(self):
        assert bucket_for_category("documents") == settings.MINIO_BUCKET_DOCUMENTS
        assert bucket_for_category("avatars") == settings.MINIO_BUCKET_AVATARS
        assert bucket_for_category("exports") == settings.MINIO_BUCKET_EXPORTS


def make_pdf(note: bytes = b"%PDF-1.4 fake pdf content") -> tuple[bytes, str]:
    return note, "application/pdf"


class TestStorageService:
    def test_ensure_buckets_creates_all_buckets_idempotently(self):
        client = FakeMinio()
        service = make_service(client)
        service.ensure_buckets()
        assert client.buckets == {
            settings.MINIO_BUCKET_DOCUMENTS,
            settings.MINIO_BUCKET_AVATARS,
            settings.MINIO_BUCKET_EXPORTS,
        }
        service.ensure_buckets()
        assert len(client.buckets) == 3

    def test_upload_round_trip(self):
        client = FakeMinio()
        service = make_service(client)
        service.ensure_buckets()
        tenant = make_tenant()
        content, content_type = make_pdf()

        stored = service.upload(
            tenant=tenant,
            category="documents",
            filename="manual.pdf",
            content=content,
            content_type=content_type,
        )

        assert isinstance(stored, StoredFile)
        assert stored.bucket == settings.MINIO_BUCKET_DOCUMENTS
        assert stored.storage_key.startswith(f"orgs/{tenant.organization_id}/documents/")
        downloaded = service.download(
            tenant=tenant,
            bucket=stored.bucket,
            storage_key=stored.storage_key,
        )
        assert downloaded == content

    def test_upload_routes_to_category_bucket(self):
        client = FakeMinio()
        service = make_service(client)
        tenant = make_tenant()
        stored = service.upload(
            tenant=tenant,
            category="avatars",
            filename="photo.txt",
            content=b"avatar",
            content_type="text/plain",
        )
        assert stored.bucket == settings.MINIO_BUCKET_AVATARS

    def test_upload_rejects_invalid_file(self):
        client = FakeMinio()
        service = make_service(client)
        with pytest.raises(FileValidationError):
            service.upload(
                tenant=make_tenant(),
                category="documents",
                filename="malware.exe",
                content=b"x",
                content_type="application/octet-stream",
            )

    def test_delete_removes_object(self):
        client = FakeMinio()
        service = make_service(client)
        tenant = make_tenant()
        stored = service.upload(
            tenant=tenant,
            category="documents",
            filename="manual.pdf",
            content=b"%PDF-1.4",
            content_type="application/pdf",
        )
        service.delete(tenant=tenant, bucket=stored.bucket, storage_key=stored.storage_key)
        with pytest.raises(FileNotFoundError):
            service.download(tenant=tenant, bucket=stored.bucket, storage_key=stored.storage_key)

    def test_download_missing_object_raises(self):
        service = make_service()
        tenant = make_tenant()
        key = generate_storage_key(tenant.organization_id, "documents", "missing.pdf")
        with pytest.raises(FileNotFoundError):
            service.download(
                tenant=tenant,
                bucket=settings.MINIO_BUCKET_DOCUMENTS,
                storage_key=key,
            )

    def test_cross_tenant_access_is_blocked(self):
        client = FakeMinio()
        service = make_service(client)
        owner_tenant = make_tenant()
        attacker_tenant = make_tenant()

        stored = service.upload(
            tenant=owner_tenant,
            category="documents",
            filename="secret.pdf",
            content=b"classified",
            content_type="application/pdf",
        )

        with pytest.raises(StorageAccessError):
            service.download(
                tenant=attacker_tenant,
                bucket=stored.bucket,
                storage_key=stored.storage_key,
            )
        with pytest.raises(StorageAccessError):
            service.delete(
                tenant=attacker_tenant,
                bucket=stored.bucket,
                storage_key=stored.storage_key,
            )
        assert client.objects[(stored.bucket, stored.storage_key)] == b"classified"


class TestSingletonAccessor:
    def test_returns_same_instance(self):
        assert get_storage_service() is get_storage_service()
