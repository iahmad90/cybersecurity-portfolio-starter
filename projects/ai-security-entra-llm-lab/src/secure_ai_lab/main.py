from functools import lru_cache
import logging
from uuid import uuid4

from fastapi import Depends, FastAPI, Header
from pydantic import BaseModel, Field

from .audit import log_security_event
from .auth import Principal, require_principal
from .config import Settings
from .providers import LLMProvider, build_provider
from .security import inspect_prompt, redact_output


@lru_cache
def get_settings() -> Settings:
    settings = Settings.from_env()
    settings.validate()
    logging.basicConfig(
        level=getattr(logging, settings.log_level, logging.INFO)
    )
    return settings


@lru_cache
def get_provider() -> LLMProvider:
    return build_provider(get_settings())


def get_principal(
    x_demo_user: str | None = Header(default=None),
    x_demo_roles: str | None = Header(default=None),
    x_ms_client_principal: str | None = Header(default=None),
) -> Principal:
    return require_principal(
        get_settings(),
        x_demo_user=x_demo_user,
        x_demo_roles=x_demo_roles,
        x_ms_client_principal=x_ms_client_principal,
    )


class ChatRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=2000)


class ChatResponse(BaseModel):
    request_id: str
    blocked: bool
    categories: list[str]
    response: str


app = FastAPI(
    title="Secure AI Gateway Lab",
    description=(
        "Portfolio lab for Entra ID, least privilege, prompt-injection "
        "defense, data protection, and privacy-safe logging."
    ),
    version="1.0.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    principal: Principal = Depends(get_principal),
    provider: LLMProvider = Depends(get_provider),
) -> ChatResponse:
    request_id = str(uuid4())
    decision = inspect_prompt(request.prompt)

    if not decision.allowed:
        log_security_event(
            event_type="input_guard",
            request_id=request_id,
            actor_id=principal.actor_id,
            decision="blocked",
            categories=decision.categories,
            prompt=request.prompt,
        )
        return ChatResponse(
            request_id=request_id,
            blocked=True,
            categories=list(decision.categories),
            response="Request blocked by AI security controls.",
        )

    raw_response = provider.generate(request.prompt)
    safe_response, redactions = redact_output(raw_response)

    log_security_event(
        event_type="chat_request",
        request_id=request_id,
        actor_id=principal.actor_id,
        decision="allowed_with_redaction" if redactions else "allowed",
        categories=redactions,
        prompt=request.prompt,
    )

    return ChatResponse(
        request_id=request_id,
        blocked=False,
        categories=list(redactions),
        response=safe_response,
    )
