from datetime import datetime, timezone
import hashlib
import json
import logging
from typing import Iterable


LOGGER = logging.getLogger("secure_ai_lab.audit")


def fingerprint(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def actor_hash(actor_id: str) -> str:
    return fingerprint(actor_id.lower())[:16]


def log_security_event(
    *,
    event_type: str,
    request_id: str,
    actor_id: str,
    decision: str,
    categories: Iterable[str] = (),
    prompt: str | None = None,
) -> dict[str, object]:
    event: dict[str, object] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "request_id": request_id,
        "actor_hash": actor_hash(actor_id),
        "decision": decision,
        "categories": list(categories),
    }

    if prompt is not None:
        event["prompt_fingerprint"] = fingerprint(prompt)
        event["prompt_length"] = len(prompt)

    LOGGER.info(json.dumps(event, sort_keys=True))
    return event
