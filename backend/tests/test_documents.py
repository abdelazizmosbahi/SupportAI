import uuid

import pytest
from sqlalchemy import Delete, Select

from app.models.document import Document
from app.services.document_service import (
    create_document,
    delete_document,
    get_document,
    list_documents,
)
from app.services.storage_service import (
    FileValidationError,
    StorageService,
    bucket_for_category,
)
from tests.test_storage_service import FakeMinio, make_tenant


def extract_filters(whereclause) -> dict[str, object]:
    clauses = [whereclause] if not hasattr(whereclause, "clauses") else list(whereclause.clauses)
    return {expr.left.name: expr.right.effective_value for expr in clauses}


class FakeDocumentDb:
    """In-memory AsyncSession stand-in for Document service tests.

    ``execute`` understands the two statements the service issues (``select``
    and ``delete`` on the ``documents`` table) and applies the WHERE filters to
    the in-memory rows.
    """

    def __init__(self):
        self.documents: list[Document] = []

    class _Scalars:
        def __init__(self, rows):
            self._rows = rows

        def all(self):
            return list(self._rows)

    class _SelectResult:
        def __init__(self, rows):
            self._rows = rows

        def scalars(self):
            return FakeDocumentDb._Scalars(self._rows)

        def scalar_one_or_none(self):
            return self._rows[0] if self._rows else None

    class _DeleteResult:
        def __init__(self, rowcount):
            self.rowcount = rowcount

    def _filter(self, rows, filters):
        return [
            row
            for row in rows
            if all(getattr(row, key) == value for key, value in filters.items())
        ]

    async def execute(self, stmt):
        if isinstance(stmt, Select):
            return self._SelectResult(
                self._filter(self.documents, extract_filters(stmt.whereclause))
            )
        if isinstance(stmt, Delete):
            before = len(self.documents)
            filters = extract_filters(stmt.whereclause)
            self.documents = [
                row
                for row in self.documents
                if not all(getattr(row, key) == value for key, value in filters.items())
            ]
            return self._DeleteResult(before - len(self.documents))
        raise NotImplementedError(stmt)

    def add(self, obj):
        if obj.id is None:
            obj.id = uuid.uuid4()
        self.documents.append(obj)

    async def flush(self):
        pass


def make_storage(client: FakeMinio) -> StorageService:
    return StorageService(
        client=client,
        bucket_names=[
            bucket_for_category("documents"),
            bucket_for_category("avatars"),
            bucket_for_category("exports"),
        ],
    )


CONTENT = b"%PDF-1.4 fake doc content"


class TestCreateDocument:
    async def test_upload_creates_document_record(self):
        client = FakeMinio()
        storage = make_storage(client)
        db = FakeDocumentDb()
        tenant = make_tenant()

        doc = await create_document(
            db,
            tenant=tenant,
            storage=storage,
            filename="manual.pdf",
            content=CONTENT,
            content_type="application/pdf",
        )

        assert doc.organization_id == tenant.organization_id
        assert doc.filename == "manual.pdf"
        assert doc.mime_type == "application/pdf"
        assert doc.storage_key.startswith(f"orgs/{tenant.organization_id}/documents/")
        assert doc.size == len(CONTENT)
        assert doc.status == "UPLOADED"
        assert doc.error_message is None
        assert doc.created_by == tenant.user_id
        assert db.documents == [doc]
        assert (bucket_for_category("documents"), doc.storage_key) in client.objects

    async def test_invalid_file_is_rejected_without_record(self):
        db = FakeDocumentDb()
        storage = make_storage(FakeMinio())
        tenant = make_tenant()

        with pytest.raises(FileValidationError):
            await create_document(
                db,
                tenant=tenant,
                storage=storage,
                filename="evil.exe",
                content=b"x",
                content_type="application/octet-stream",
            )
        assert db.documents == []

    async def test_mime_type_falls_back_to_guessed(self):
        db = FakeDocumentDb()
        storage = make_storage(FakeMinio())
        tenant = make_tenant()

        doc = await create_document(
            db,
            tenant=tenant,
            storage=storage,
            filename="notes.pdf",
            content=CONTENT,
            content_type=None,
        )
        assert doc.mime_type == "application/pdf"


class TestListAndGet:
    async def test_list_returns_only_org_documents(self):
        db = FakeDocumentDb()
        storage = make_storage(FakeMinio())
        tenant_a = make_tenant()
        tenant_b = make_tenant()

        doc_a1 = await create_document(
            db, tenant=tenant_a, storage=storage, filename="a1.pdf",
            content=CONTENT, content_type="application/pdf",
        )
        doc_a2 = await create_document(
            db, tenant=tenant_a, storage=storage, filename="a2.txt",
            content=b"hello", content_type="text/plain",
        )
        doc_b = await create_document(
            db, tenant=tenant_b, storage=storage, filename="b.pdf",
            content=CONTENT, content_type="application/pdf",
        )

        org_a_ids = {d.id for d in await list_documents(db, tenant_a.organization_id)}
        assert org_a_ids == {doc_a1.id, doc_a2.id}
        assert {d.id for d in await list_documents(db, tenant_b.organization_id)} == {doc_b.id}

    async def test_get_is_scoped_by_organization(self):
        db = FakeDocumentDb()
        storage = make_storage(FakeMinio())
        tenant = make_tenant()
        other_org = tenant.organization_id
        doc = await create_document(
            db, tenant=tenant, storage=storage, filename="manual.pdf",
            content=CONTENT, content_type="application/pdf",
        )

        assert (await get_document(db, other_org, doc.id)) is doc
        assert await get_document(db, uuid.uuid4(), doc.id) is None


class TestDeleteDocument:
    async def test_delete_removes_record_and_object(self):
        client = FakeMinio()
        storage = make_storage(client)
        db = FakeDocumentDb()
        tenant = make_tenant()
        doc = await create_document(
            db, tenant=tenant, storage=storage, filename="manual.pdf",
            content=CONTENT, content_type="application/pdf",
        )

        await delete_document(db, tenant=tenant, storage=storage, document=doc)

        assert db.documents == []
        assert (bucket_for_category("documents"), doc.storage_key) not in client.objects

    async def test_delete_tolerates_missing_object(self):
        client = FakeMinio()
        storage = make_storage(client)
        db = FakeDocumentDb()
        tenant = make_tenant()
        doc = await create_document(
            db, tenant=tenant, storage=storage, filename="manual.pdf",
            content=CONTENT, content_type="application/pdf",
        )
        client.objects.pop((bucket_for_category("documents"), doc.storage_key), None)

        await delete_document(db, tenant=tenant, storage=storage, document=doc)

        assert db.documents == []
