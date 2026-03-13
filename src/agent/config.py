"""Configuration for aloop."""

import os


class Config:
    """All configuration from environment variables with sensible defaults."""

    # Azure OpenAI
    AZURE_OPENAI_ENDPOINT: str = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
    AZURE_OPENAI_API_VERSION: str = os.environ.get(
        "AZURE_OPENAI_API_VERSION", "2025-03-01-preview"
    )
    AZURE_OPENAI_DEPLOYMENT: str = os.environ.get(
        "AZURE_OPENAI_DEPLOYMENT", "gpt-5.3-chat"
    )

    # Azure Blob Storage
    AZURE_STORAGE_ACCOUNT_NAME: str = os.environ.get(
        "AZURE_STORAGE_ACCOUNT_NAME", ""
    )
    AZURE_STORAGE_CONTAINER: str = os.environ.get(
        "AZURE_STORAGE_CONTAINER", "agent-workspace"
    )

    # Loop settings (defaults, overridden by steering.md)
    DEFAULT_INTERVAL_MINUTES: int = int(
        os.environ.get("LOOP_INTERVAL_MINUTES", "10")
    )
    DEFAULT_MAX_ITERATIONS: int = int(
        os.environ.get("LOOP_MAX_ITERATIONS", "50")
    )
    DEFAULT_TARGET_SCORE: int = int(
        os.environ.get("LOOP_TARGET_SCORE", "90")
    )

    # Agent identity
    AGENT_NAME: str = os.environ.get("AGENT_NAME", "aloop")

    # Local mode (for development without Azure)
    LOCAL_MODE: bool = os.environ.get("LOCAL_MODE", "false").lower() == "true"
    LOCAL_WORKSPACE: str = os.environ.get("LOCAL_WORKSPACE", "./workspace")

    @classmethod
    def validate(cls) -> list[str]:
        """Return list of missing required config."""
        errors = []
        if not cls.LOCAL_MODE:
            if not cls.AZURE_OPENAI_ENDPOINT:
                errors.append("AZURE_OPENAI_ENDPOINT is required")
            if not cls.AZURE_STORAGE_ACCOUNT_NAME:
                errors.append("AZURE_STORAGE_ACCOUNT_NAME is required")
        return errors
