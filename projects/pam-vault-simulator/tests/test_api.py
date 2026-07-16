from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient

from pam_vault_simulator.main import create_app
from pam_vault_simulator.vault import Vault, VaultAccount


class MutableClock:
    def __init__(self) -> None:
        self.current = datetime(2026, 7, 16, tzinfo=timezone.utc)

    def __call__(self) -> datetime:
        return self.current

    def advance(self, *, seconds: int) -> None:
        self.current += timedelta(seconds=seconds)


def build_test_client() -> tuple[TestClient, Vault, MutableClock]:
    clock = MutableClock()
    vault = Vault(
        accounts={
            "server-admin": VaultAccount(
                account_id="server-admin",
                username="administrator",
                secret="before-rotation",
                allowed_actors={"alice"},
            )
        },
        clock=clock,
        secret_factory=lambda: "after-rotation",
    )
    return TestClient(create_app(vault)), vault, clock


PAM_HEADERS = {
    "X-Demo-Actor": "alice",
    "X-Demo-Roles": "PAM-Users",
}
AUDIT_HEADERS = {
    "X-Demo-Actor": "auditor",
    "X-Demo-Roles": "PAM-Auditors",
}


def test_checkout_returns_time_limited_credential_lease() -> None:
    client, _, _ = build_test_client()

    response = client.post(
        "/accounts/server-admin/checkout",
        headers=PAM_HEADERS,
        json={"duration_seconds": 120},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["account_id"] == "server-admin"
    assert body["username"] == "administrator"
    assert body["credential"] == "before-rotation"
    assert body["credential_version"] == 1
    assert body["expires_at"] == "2026-07-16T00:02:00+00:00"


def test_checkout_enforces_account_level_least_privilege() -> None:
    client, _, _ = build_test_client()

    response = client.post(
        "/accounts/server-admin/checkout",
        headers={
            "X-Demo-Actor": "bob",
            "X-Demo-Roles": "PAM-Users",
        },
        json={"duration_seconds": 120},
    )

    assert response.status_code == 403


def test_checkin_rotates_mock_credential() -> None:
    client, vault, _ = build_test_client()
    checkout = client.post(
        "/accounts/server-admin/checkout",
        headers=PAM_HEADERS,
        json={"duration_seconds": 120},
    )
    lease_id = checkout.json()["lease_id"]

    response = client.post(
        f"/leases/{lease_id}/checkin",
        headers=PAM_HEADERS,
    )

    assert response.status_code == 200
    assert response.json()["status"] == "checked_in"
    assert response.json()["credential_rotated"] is True
    assert response.json()["credential_version"] == 2
    assert vault.accounts["server-admin"].secret == "after-rotation"


def test_expired_lease_is_denied_and_not_rotated() -> None:
    client, vault, clock = build_test_client()
    checkout = client.post(
        "/accounts/server-admin/checkout",
        headers=PAM_HEADERS,
        json={"duration_seconds": 30},
    )
    lease_id = checkout.json()["lease_id"]
    clock.advance(seconds=31)

    response = client.post(
        f"/leases/{lease_id}/checkin",
        headers=PAM_HEADERS,
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "Expired leases cannot be used for check-in."
    )
    assert vault.accounts["server-admin"].secret == "before-rotation"
    assert vault.leases[lease_id].status == "expired"


def test_audit_log_records_checkout_and_checkin() -> None:
    client, _, _ = build_test_client()
    checkout = client.post(
        "/accounts/server-admin/checkout",
        headers=PAM_HEADERS,
        json={"duration_seconds": 120},
    )
    lease_id = checkout.json()["lease_id"]
    client.post(f"/leases/{lease_id}/checkin", headers=PAM_HEADERS)

    response = client.get("/audit", headers=AUDIT_HEADERS)

    assert response.status_code == 200
    events = response.json()
    assert [(event["event_type"], event["outcome"]) for event in events] == [
        ("checkout", "success"),
        ("checkin", "success"),
    ]
    assert all(event["account_id"] == "server-admin" for event in events)
    assert all(event["lease_id"] == lease_id for event in events)
    assert events[1]["detail"] == "credential_rotated;version=2"


def test_expired_checkin_denial_is_audited() -> None:
    client, _, clock = build_test_client()
    checkout = client.post(
        "/accounts/server-admin/checkout",
        headers=PAM_HEADERS,
        json={"duration_seconds": 10},
    )
    lease_id = checkout.json()["lease_id"]
    clock.advance(seconds=10)
    client.post(f"/leases/{lease_id}/checkin", headers=PAM_HEADERS)

    events = client.get("/audit", headers=AUDIT_HEADERS).json()

    assert events[-1]["event_type"] == "checkin"
    assert events[-1]["outcome"] == "denied"
    assert events[-1]["detail"] == "lease_expired"


def test_audit_endpoint_requires_auditor_role() -> None:
    client, _, _ = build_test_client()

    response = client.get("/audit", headers=PAM_HEADERS)

    assert response.status_code == 403
