from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from threading import RLock
from typing import Callable
from uuid import uuid4

from fastapi import HTTPException, status


Clock = Callable[[], datetime]
SecretFactory = Callable[[], str]


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def generate_mock_secret() -> str:
    return f"mock-{uuid4().hex}"


@dataclass
class VaultAccount:
    account_id: str
    username: str
    secret: str
    allowed_actors: set[str]
    credential_version: int = 1


@dataclass
class Lease:
    lease_id: str
    account_id: str
    actor: str
    checked_out_at: datetime
    expires_at: datetime
    status: str = "active"


@dataclass(frozen=True)
class AuditEvent:
    timestamp: datetime
    event_type: str
    outcome: str
    actor: str
    account_id: str
    lease_id: str | None
    detail: str


@dataclass
class Vault:
    accounts: dict[str, VaultAccount]
    clock: Clock = utc_now
    secret_factory: SecretFactory = generate_mock_secret
    leases: dict[str, Lease] = field(default_factory=dict)
    audit_events: list[AuditEvent] = field(default_factory=list)
    _lock: RLock = field(default_factory=RLock)

    def checkout(
        self,
        *,
        account_id: str,
        actor: str,
        duration_seconds: int,
    ) -> tuple[Lease, VaultAccount]:
        with self._lock:
            account = self._get_account(account_id)
            now = self.clock()

            if actor not in account.allowed_actors:
                self._audit(
                    now=now,
                    event_type="checkout",
                    outcome="denied",
                    actor=actor,
                    account_id=account_id,
                    lease_id=None,
                    detail="actor_not_authorized",
                )
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Actor is not authorized for this account.",
                )

            active_lease = self._active_lease_for(account_id, now)
            if active_lease is not None:
                self._audit(
                    now=now,
                    event_type="checkout",
                    outcome="denied",
                    actor=actor,
                    account_id=account_id,
                    lease_id=active_lease.lease_id,
                    detail="account_already_checked_out",
                )
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Account already has an active lease.",
                )

            lease = Lease(
                lease_id=str(uuid4()),
                account_id=account_id,
                actor=actor,
                checked_out_at=now,
                expires_at=now + timedelta(seconds=duration_seconds),
            )
            self.leases[lease.lease_id] = lease
            self._audit(
                now=now,
                event_type="checkout",
                outcome="success",
                actor=actor,
                account_id=account_id,
                lease_id=lease.lease_id,
                detail=f"lease_seconds={duration_seconds}",
            )
            return lease, account

    def checkin(self, *, lease_id: str, actor: str) -> tuple[Lease, VaultAccount]:
        with self._lock:
            lease = self.leases.get(lease_id)
            now = self.clock()

            if lease is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Lease not found.",
                )

            if lease.actor != actor:
                self._audit(
                    now=now,
                    event_type="checkin",
                    outcome="denied",
                    actor=actor,
                    account_id=lease.account_id,
                    lease_id=lease_id,
                    detail="lease_owner_mismatch",
                )
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only the lease owner can check in this credential.",
                )

            if lease.status != "active":
                self._audit(
                    now=now,
                    event_type="checkin",
                    outcome="denied",
                    actor=actor,
                    account_id=lease.account_id,
                    lease_id=lease_id,
                    detail=f"lease_status={lease.status}",
                )
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Lease is not active.",
                )

            if now >= lease.expires_at:
                lease.status = "expired"
                self._audit(
                    now=now,
                    event_type="checkin",
                    outcome="denied",
                    actor=actor,
                    account_id=lease.account_id,
                    lease_id=lease_id,
                    detail="lease_expired",
                )
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Expired leases cannot be used for check-in.",
                )

            account = self._get_account(lease.account_id)
            account.secret = self.secret_factory()
            account.credential_version += 1
            lease.status = "checked_in"
            self._audit(
                now=now,
                event_type="checkin",
                outcome="success",
                actor=actor,
                account_id=lease.account_id,
                lease_id=lease_id,
                detail=(
                    "credential_rotated;"
                    f"version={account.credential_version}"
                ),
            )
            return lease, account

    def list_audit_events(self) -> tuple[AuditEvent, ...]:
        with self._lock:
            return tuple(self.audit_events)

    def _get_account(self, account_id: str) -> VaultAccount:
        account = self.accounts.get(account_id)
        if account is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vault account not found.",
            )
        return account

    def _active_lease_for(
        self,
        account_id: str,
        now: datetime,
    ) -> Lease | None:
        for lease in self.leases.values():
            if lease.account_id != account_id or lease.status != "active":
                continue
            if now >= lease.expires_at:
                lease.status = "expired"
                continue
            return lease
        return None

    def _audit(
        self,
        *,
        now: datetime,
        event_type: str,
        outcome: str,
        actor: str,
        account_id: str,
        lease_id: str | None,
        detail: str,
    ) -> None:
        self.audit_events.append(
            AuditEvent(
                timestamp=now,
                event_type=event_type,
                outcome=outcome,
                actor=actor,
                account_id=account_id,
                lease_id=lease_id,
                detail=detail,
            )
        )


def build_demo_vault() -> Vault:
    return Vault(
        accounts={
            "linux-root": VaultAccount(
                account_id="linux-root",
                username="root",
                secret="Initial-Mock-Secret-1",
                allowed_actors={"pam-analyst", "linux-admin"},
            ),
            "database-admin": VaultAccount(
                account_id="database-admin",
                username="dbadmin",
                secret="Initial-Mock-Secret-2",
                allowed_actors={"pam-analyst", "database-admin"},
            ),
        }
    )
