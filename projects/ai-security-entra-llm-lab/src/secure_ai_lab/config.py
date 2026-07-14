from dataclasses import dataclass
import os


def _env(name: str, default: str) -> str:
    return os.getenv(name, default).strip()


@dataclass(frozen=True)
class Settings:
    auth_mode: str
    provider: str
    allowed_role: str
    log_level: str
    azure_openai_base_url: str
    azure_openai_deployment: str
    website_auth_enabled: bool

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            auth_mode=_env("LAB_AUTH_MODE", "demo").lower(),
            provider=_env("LAB_PROVIDER", "local").lower(),
            allowed_role=_env("LAB_ALLOWED_ROLE", "AI-Lab-Users"),
            log_level=_env("LAB_LOG_LEVEL", "INFO").upper(),
            azure_openai_base_url=_env("AZURE_OPENAI_BASE_URL", ""),
            azure_openai_deployment=_env("AZURE_OPENAI_DEPLOYMENT", ""),
            website_auth_enabled=_env("WEBSITE_AUTH_ENABLED", "False").lower()
            == "true",
        )

    def validate(self) -> None:
        if self.auth_mode not in {"demo", "entra_proxy"}:
            raise ValueError("LAB_AUTH_MODE must be demo or entra_proxy")
        if self.provider not in {"local", "azure"}:
            raise ValueError("LAB_PROVIDER must be local or azure")
        if self.auth_mode == "entra_proxy" and not self.website_auth_enabled:
            raise ValueError(
                "entra_proxy requires WEBSITE_AUTH_ENABLED=True"
            )
        if self.provider == "azure":
            if not self.azure_openai_base_url:
                raise ValueError("AZURE_OPENAI_BASE_URL is required")
            if not self.azure_openai_deployment:
                raise ValueError("AZURE_OPENAI_DEPLOYMENT is required")
            if not self.azure_openai_base_url.endswith("/openai/v1/"):
                raise ValueError(
                    "AZURE_OPENAI_BASE_URL must end with /openai/v1/"
                )
