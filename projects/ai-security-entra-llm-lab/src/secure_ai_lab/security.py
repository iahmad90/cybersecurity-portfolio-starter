from dataclasses import dataclass
import re


@dataclass(frozen=True)
class GuardDecision:
    allowed: bool
    categories: tuple[str, ...]


INJECTION_PATTERNS = (
    re.compile(
        r"\b(ignore|disregard|forget|override)\b.{0,45}"
        r"\b(previous|prior|system|developer|security)\b.{0,25}"
        r"\b(instruction|prompt|rule|policy)s?\b",
        re.IGNORECASE | re.DOTALL,
    ),
    re.compile(
        r"\b(reveal|repeat|print|show|expose)\b.{0,35}"
        r"\b(system|developer|hidden|internal)\b.{0,20}"
        r"\b(prompt|instruction|message|policy)s?\b",
        re.IGNORECASE | re.DOTALL,
    ),
    re.compile(
        r"\b(jailbreak|developer mode|do anything now|DAN mode)\b",
        re.IGNORECASE,
    ),
)

EXFILTRATION_PATTERN = re.compile(
    r"\b(reveal|show|list|print|return|send|exfiltrate)\b.{0,60}"
    r"\b(api[- ]?key|password|secret|access token|bearer token|"
    r"private key|conversation history|previous user data)s?\b",
    re.IGNORECASE | re.DOTALL,
)

SENSITIVE_INPUT_PATTERNS = {
    "ssn": re.compile(r"(?<!\d)\d{3}-\d{2}-\d{4}(?!\d)"),
    "credit_card": re.compile(
        r"(?<!\d)(?:\d[ -]*?){13,19}(?!\d)"
    ),
    "bearer_token": re.compile(
        r"\bBearer\s+[A-Za-z0-9._~+/=-]{16,}", re.IGNORECASE
    ),
    "private_key": re.compile(
        r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
    ),
    "api_key": re.compile(
        r"\b(?:api[-_ ]?key|secret[-_ ]?key)\s*[:=]\s*"
        r"[A-Za-z0-9._-]{12,}",
        re.IGNORECASE,
    ),
}

OUTPUT_REDACTIONS = (
    (
        re.compile(r"(?<!\d)\d{3}-\d{2}-\d{4}(?!\d)"),
        "[REDACTED_SSN]",
    ),
    (
        re.compile(
            r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
            re.IGNORECASE,
        ),
        "[REDACTED_EMAIL]",
    ),
    (
        re.compile(
            r"\bBearer\s+[A-Za-z0-9._~+/=-]{16,}", re.IGNORECASE
        ),
        "[REDACTED_TOKEN]",
    ),
    (
        re.compile(
            r"\b(?:api[-_ ]?key|secret[-_ ]?key)\s*[:=]\s*"
            r"[A-Za-z0-9._-]{12,}",
            re.IGNORECASE,
        ),
        "[REDACTED_SECRET]",
    ),
    (
        re.compile(
            r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
            r".*?-----END (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
            re.DOTALL,
        ),
        "[REDACTED_PRIVATE_KEY]",
    ),
)


def inspect_prompt(prompt: str) -> GuardDecision:
    categories: set[str] = set()

    if any(pattern.search(prompt) for pattern in INJECTION_PATTERNS):
        categories.add("prompt_injection")

    if EXFILTRATION_PATTERN.search(prompt):
        categories.add("secret_exfiltration")

    for name, pattern in SENSITIVE_INPUT_PATTERNS.items():
        if pattern.search(prompt):
            categories.add(f"sensitive_input:{name}")

    return GuardDecision(
        allowed=not categories,
        categories=tuple(sorted(categories)),
    )


def redact_output(text: str) -> tuple[str, tuple[str, ...]]:
    redacted = text
    categories: list[str] = []

    for pattern, replacement in OUTPUT_REDACTIONS:
        updated, count = pattern.subn(replacement, redacted)
        if count:
            categories.append(replacement.strip("[]").lower())
            redacted = updated

    return redacted, tuple(categories)
