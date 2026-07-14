from base64 import b64decode
from dataclasses import dataclass
import json

from fastapi import Header, HTTPException, status

from .config import Settings


@dataclass(frozen=True)
class Principal:
    actor_id: str
    roles: frozenset[str]
    source: str


def _parse_entra_principal(encoded_principal: str) -> Principal:
    try:
        padding = "=" * (-len(encoded_principal) % 4)
        payload = json.loads(b64decode(encoded_principal + padding))
        claims = payload.get("claims", [])
        claim_map: dict[str, list[str]] = {}

        for claim in claims:
            claim_map.setdefault(claim["typ"], []).append(claim["val"])

        actor_id = (
            claim_map.get(
                "http://schemas.microsoft.com/identity/claims/objectidentifier",
                [""],
            )[0]
            or claim_map.get(
                "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name",
                [""],
            )[0]
        )
        roles = frozenset(
            claim_map.get(
                "http://schemas.microsoft.com/ws/2008/06/identity/claims/role",
                [],
            )
        )
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Entra principal",
        ) from exc

    if not actor_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Entra principal has no actor identifier",
        )

    return Principal(actor_id=actor_id, roles=roles, source="entra_proxy")


def build_principal(
    settings: Settings,
    *,
    demo_user: str | None,
    demo_roles: str | None,
    entra_principal: str | None,
) -> Principal:
    if settings.auth_mode == "demo":
        if not demo_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="X-Demo-User is required in demo mode",
            )
        roles = frozenset(
            role.strip()
            for role in (demo_roles or "").split(",")
            if role.strip()
        )
        return Principal(
            actor_id=demo_user,
            roles=roles,
            source="demo",
        )

    if not entra_principal:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authenticated Entra principal is required",
        )

    return _parse_entra_principal(entra_principal)


def require_principal(
    settings: Settings,
    *,
    x_demo_user: str | None = Header(default=None),
    x_demo_roles: str | None = Header(default=None),
    x_ms_client_principal: str | None = Header(default=None),
) -> Principal:
    principal = build_principal(
        settings,
        demo_user=x_demo_user,
        demo_roles=x_demo_roles,
        entra_principal=x_ms_client_principal,
    )

    if settings.allowed_role not in principal.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Required role: {settings.allowed_role}",
        )

    return principal
