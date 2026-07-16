from fastapi import Depends, FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field

from .vault import AuditEvent, Vault, build_demo_vault


class Principal(BaseModel):
    actor: str
    roles: set[str]


class CheckoutRequest(BaseModel):
    duration_seconds: int = Field(default=300, ge=1, le=3600)


class CheckoutResponse(BaseModel):
    lease_id: str
    account_id: str
    username: str
    credential: str
    credential_version: int
    expires_at: str


class CheckinResponse(BaseModel):
    lease_id: str
    account_id: str
    status: str
    credential_rotated: bool
    credential_version: int


class AuditEventResponse(BaseModel):
    timestamp: str
    event_type: str
    outcome: str
    actor: str
    account_id: str
    lease_id: str | None
    detail: str


def get_principal(
    x_demo_actor: str | None = Header(default=None),
    x_demo_roles: str | None = Header(default=None),
) -> Principal:
    if not x_demo_actor:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="X-Demo-Actor header is required.",
        )
    roles = {
        role.strip()
        for role in (x_demo_roles or "").split(",")
        if role.strip()
    }
    return Principal(actor=x_demo_actor, roles=roles)


def require_role(principal: Principal, role: str) -> None:
    if role not in principal.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"{role} role is required.",
        )


def audit_response(event: AuditEvent) -> AuditEventResponse:
    return AuditEventResponse(
        timestamp=event.timestamp.isoformat(),
        event_type=event.event_type,
        outcome=event.outcome,
        actor=event.actor,
        account_id=event.account_id,
        lease_id=event.lease_id,
        detail=event.detail,
    )


def create_app(vault: Vault | None = None) -> FastAPI:
    active_vault = vault or build_demo_vault()
    app = FastAPI(
        title="PAM Vault Simulator",
        description=(
            "Local portfolio lab for privileged credential vaulting, "
            "time-limited checkout, check-in, rotation, and auditing."
        ),
        version="1.0.0",
    )

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post(
        "/accounts/{account_id}/checkout",
        response_model=CheckoutResponse,
    )
    def checkout(
        account_id: str,
        request: CheckoutRequest,
        principal: Principal = Depends(get_principal),
    ) -> CheckoutResponse:
        require_role(principal, "PAM-Users")
        lease, account = active_vault.checkout(
            account_id=account_id,
            actor=principal.actor,
            duration_seconds=request.duration_seconds,
        )
        return CheckoutResponse(
            lease_id=lease.lease_id,
            account_id=account.account_id,
            username=account.username,
            credential=account.secret,
            credential_version=account.credential_version,
            expires_at=lease.expires_at.isoformat(),
        )

    @app.post(
        "/leases/{lease_id}/checkin",
        response_model=CheckinResponse,
    )
    def checkin(
        lease_id: str,
        principal: Principal = Depends(get_principal),
    ) -> CheckinResponse:
        require_role(principal, "PAM-Users")
        lease, account = active_vault.checkin(
            lease_id=lease_id,
            actor=principal.actor,
        )
        return CheckinResponse(
            lease_id=lease.lease_id,
            account_id=account.account_id,
            status=lease.status,
            credential_rotated=True,
            credential_version=account.credential_version,
        )

    @app.get("/audit", response_model=list[AuditEventResponse])
    def audit(
        principal: Principal = Depends(get_principal),
    ) -> list[AuditEventResponse]:
        require_role(principal, "PAM-Auditors")
        return [
            audit_response(event)
            for event in active_vault.list_audit_events()
        ]

    return app


app = create_app()
