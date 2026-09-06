import uuid

import pytest
from fastapi import HTTPException

from app.core import permissions as perm
from app.core.tenant import TenantContext, resolve_tenant
from app.models.membership import Membership
from app.models.role import Role


def make_role(name: str, perms: list[str]) -> Role:
    return Role(name=name, permissions=perms)


def make_membership(user_id: uuid.UUID, org_id: uuid.UUID) -> Membership:
    return Membership(
        id=uuid.uuid4(),
        user_id=user_id,
        organization_id=org_id,
        role_id=uuid.uuid4(),
    )


def make_context(membership: Membership, role_name: str, perms: list[str]) -> TenantContext:
    return TenantContext(
        membership=membership,
        user_id=membership.user_id,
        organization_id=membership.organization_id,
        role_id=membership.role_id,
        role_name=role_name,
        permissions=set(perms),
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
        return make_membership(uuid.uuid4(), uuid.uuid4())

    async def test_allows_member_with_permission(self, monkeypatch, actor):
        context = make_context(actor, "ADMIN", [perm.PERMISSION_MEMBERS_UPDATE])

        async def fake_resolve_tenant(db, user_id, org_id):
            return context

        monkeypatch.setattr(perm, "resolve_tenant", fake_resolve_tenant)

        checker = perm.require_permission(perm.PERMISSION_MEMBERS_UPDATE)
        result = await checker(
            org_id=actor.organization_id,
            request=None,
            current_user=type("U", (), {"id": actor.user_id})(),
            db=object(),
        )
        assert result is actor

    async def test_forbids_missing_permission(self, monkeypatch, actor):
        context = make_context(actor, "VIEWER", [perm.PERMISSION_MEMBERS_READ])

        async def fake_resolve_tenant(db, user_id, org_id):
            return context

        monkeypatch.setattr(perm, "resolve_tenant", fake_resolve_tenant)

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
        context = make_context(actor, "GHOST", [])

        async def fake_resolve_tenant(db, user_id, org_id):
            return context

        monkeypatch.setattr(perm, "resolve_tenant", fake_resolve_tenant)

        checker = perm.require_permission(perm.PERMISSION_ANALYTICS_READ)
        with pytest.raises(HTTPException) as exc:
            await checker(
                org_id=actor.organization_id,
                request=None,
                current_user=type("U", (), {"id": actor.user_id})(),
                db=object(),
            )
        assert exc.value.status_code == 403


class FakeMembershipDb:
    """Fake AsyncSession backed by a {(user_id, org_id): Membership} map.

    ``execute`` parses the membership query's WHERE bind values and returns
    exactly what the query would find in that map. This doubles as an assertion
    that resolve_tenant always filters the membership lookup by both the user
    and the organization.
    """

    def __init__(self, memberships_by_pair: dict[tuple[uuid.UUID, uuid.UUID], Membership]):
        self.memberships = memberships_by_pair
        self.roles: dict[uuid.UUID, Role | None] = {}

    class _Result:
        def __init__(self, value):
            self._value = value

        def scalar_one_or_none(self):
            return self._value

    async def execute(self, stmt):
        where = stmt.whereclause
        clauses = where.clauses if hasattr(where, "clauses") else [where]
        binds = [expr.right.effective_value for expr in clauses]
        pair = tuple(binds[:2])
        return self._Result(self.memberships.get(pair))

    async def get(self, model, role_id):
        return self.roles.get(role_id)


class TestTenantIsolation:
    """Cross-tenant access must be blocked at the resolve_tenant boundary."""

    @pytest.mark.asyncio
    async def test_blocks_access_to_foreign_organization(self):
        user_id = uuid.uuid4()
        own_org = uuid.uuid4()
        foreign_org = uuid.uuid4()
        own_membership = make_membership(user_id, own_org)

        # User is a member of own_org only. resolve_tenant(user, foreign_org)
        # can never find a membership because the query is scoped by both keys.
        db = FakeMembershipDb({(user_id, own_org): own_membership})
        with pytest.raises(HTTPException) as exc:
            await resolve_tenant(db, user_id, foreign_org)
        assert exc.value.status_code == 403

    @pytest.mark.asyncio
    async def test_allows_access_to_own_organization(self):
        user_id = uuid.uuid4()
        org_id = uuid.uuid4()
        membership = make_membership(user_id, org_id)
        role = make_role("OWNER", perm.ALL_PERMISSIONS)

        db = FakeMembershipDb({(user_id, org_id): membership})
        db.roles[membership.role_id] = role

        context = await resolve_tenant(db, user_id, org_id)
        assert context.membership is membership
        assert context.role_name == "OWNER"
        assert perm.PERMISSION_MEMBERS_READ in context.permissions

    @pytest.mark.asyncio
    async def test_scope_requires_both_user_and_org(self):
        """A foreign user cannot resolve a context even for a known org."""
        user_a = uuid.uuid4()
        user_b = uuid.uuid4()
        org_id = uuid.uuid4()
        membership = make_membership(user_a, org_id)

        db = FakeMembershipDb({(user_a, org_id): membership})
        with pytest.raises(HTTPException) as exc:
            await resolve_tenant(db, user_b, org_id)
        assert exc.value.status_code == 403
