import uuid

import pytest
from fastapi import HTTPException

from app.core import permissions as perm
from app.models.membership import Membership
from app.models.role import Role


def make_role(name: str, perms: list[str]) -> Role:
    return Role(name=name, permissions=perms)


def make_membership(user_id: uuid.UUID) -> Membership:
    return Membership(
        id=uuid.uuid4(),
        user_id=user_id,
        organization_id=uuid.uuid4(),
        role_id=uuid.uuid4(),
    )


class TestPermissionMatrix:
    """OWNER / ADMIN / AGENT / VIEWER role permissions."""

    def test_owner_has_all_permissions(self):
        owner_perms = perm.role_permissions(perm.ROLE_OWNER)
        assert perm.PERMISSION_ORGANIZATION_DELETE in owner_perms
        assert perm.PERMISSION_MEMBERS_DELETE in owner_perms
        assert owner_perms == set(perm.ALL_PERMISSIONS)

    def test_admin_can_manage_members_but_no_delete_org(self):
        admin_perms = perm.role_permissions(perm.ROLE_ADMIN)
        assert perm.PERMISSION_MEMBERS_CREATE in admin_perms
        assert perm.PERMISSION_MEMBERS_DELETE in admin_perms
        assert perm.PERMISSION_ORGANIZATION_DELETE not in admin_perms

    def test_agent_only_conversations(self):
        agent_perms = perm.role_permissions(perm.ROLE_AGENT)
        assert perm.PERMISSION_CONVERSATIONS_CREATE in agent_perms
        assert perm.PERMISSION_CONVERSATIONS_ASSIGN in agent_perms
        assert perm.PERMISSION_MEMBERS_READ not in agent_perms
        assert perm.PERMISSION_ORGANIZATION_UPDATE not in agent_perms

    def test_viewer_read_only(self):
        viewer_perms = perm.role_permissions(perm.ROLE_VIEWER)
        for write_perm in (
            perm.PERMISSION_MEMBERS_CREATE,
            perm.PERMISSION_MEMBERS_UPDATE,
            perm.PERMISSION_MEMBERS_DELETE,
            perm.PERMISSION_ORGANIZATION_UPDATE,
            perm.PERMISSION_CONVERSATIONS_CREATE,
            perm.PERMISSION_MESSAGES_CREATE,
            perm.PERMISSION_TICKETS_CREATE,
        ):
            assert write_perm not in viewer_perms
        assert perm.PERMISSION_MEMBERS_READ in viewer_perms
        assert perm.PERMISSION_ANALYTICS_READ in viewer_perms

    def test_each_role_is_covered_by_role_permissions_map(self):
        assert set(perm.ROLE_PERMISSIONS_MAP.keys()) == perm.ROLE_NAMES


class TestRequirePermission:
    @pytest.fixture
    def actor(self):
        return make_membership(uuid.uuid4())

    async def test_allows_member_with_permission(self, monkeypatch, actor):
        async def fake_get_membership(db, user_id, org_id):
            return actor

        async def fake_resolve_role(db, role_id):
            return make_role("ADMIN", [perm.PERMISSION_MEMBERS_UPDATE])

        monkeypatch.setattr(perm, "_get_membership", fake_get_membership)
        monkeypatch.setattr(perm, "_resolve_role", fake_resolve_role)

        checker = perm.require_permission(perm.PERMISSION_MEMBERS_UPDATE)
        result = await checker(
            org_id=actor.organization_id,
            request=None,
            current_user=type("U", (), {"id": actor.user_id})(),
            db=object(),
        )
        assert result is actor

    async def test_forbids_non_member(self, monkeypatch, actor):
        async def fake_get_membership(db, user_id, org_id):
            return None

        monkeypatch.setattr(perm, "_get_membership", fake_get_membership)

        checker = perm.require_permission(perm.PERMISSION_MEMBERS_READ)
        with pytest.raises(HTTPException) as exc:
            await checker(
                org_id=actor.organization_id,
                request=None,
                current_user=type("U", (), {"id": actor.user_id})(),
                db=object(),
            )
        assert exc.value.status_code == 403

    async def test_forbids_missing_permission(self, monkeypatch, actor):
        async def fake_get_membership(db, user_id, org_id):
            return actor

        async def fake_resolve_role(db, role_id):
            return make_role("VIEWER", [perm.PERMISSION_MEMBERS_READ])

        monkeypatch.setattr(perm, "_get_membership", fake_get_membership)
        monkeypatch.setattr(perm, "_resolve_role", fake_resolve_role)

        checker = perm.require_permission(perm.PERMISSION_MEMBERS_CREATE)
        with pytest.raises(HTTPException) as exc:
            await checker(
                org_id=actor.organization_id,
                request=None,
                current_user=type("U", (), {"id": actor.user_id})(),
                db=object(),
            )
        assert exc.value.status_code == 403

    async def test_forbids_unknown_role(self, monkeypatch, actor):
        async def fake_get_membership(db, user_id, org_id):
            return actor

        async def fake_resolve_role(db, role_id):
            return make_role("GHOST", [])

        monkeypatch.setattr(perm, "_get_membership", fake_get_membership)
        monkeypatch.setattr(perm, "_resolve_role", fake_resolve_role)

        checker = perm.require_permission(perm.PERMISSION_ANALYTICS_READ)
        with pytest.raises(HTTPException) as exc:
            await checker(
                org_id=actor.organization_id,
                request=None,
                current_user=type("U", (), {"id": actor.user_id})(),
                db=object(),
            )
        assert exc.value.status_code == 403
