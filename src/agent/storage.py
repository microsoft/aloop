"""Storage abstraction — Azure Blob or local filesystem."""

from __future__ import annotations

import json
import os
from pathlib import Path

from config import Config


class Storage:
    """Read/write files to Azure Blob Storage or local filesystem."""

    def __init__(self) -> None:
        if Config.LOCAL_MODE:
            self._backend = _LocalBackend(Config.LOCAL_WORKSPACE)
        else:
            self._backend = _BlobBackend(
                Config.AZURE_STORAGE_ACCOUNT_NAME,
                Config.AZURE_STORAGE_CONTAINER,
            )

    def read(self, path: str) -> str | None:
        """Read a text file. Returns None if not found."""
        return self._backend.read(path)

    def write(self, path: str, content: str) -> None:
        """Write a text file, creating parent dirs/containers as needed."""
        self._backend.write(path, content)

    def append(self, path: str, content: str) -> None:
        """Append to a text file (read + write)."""
        existing = self.read(path) or ""
        self.write(path, existing + content)

    def list_files(self, prefix: str = "") -> list[str]:
        """List files under a prefix."""
        return self._backend.list_files(prefix)

    def read_json(self, path: str) -> dict | list | None:
        """Read and parse a JSON file. Raises JSONDecodeError on malformed content."""
        raw = self.read(path)
        if raw is None:
            return None
        return json.loads(raw.strip())

    def write_json(self, path: str, data: dict | list) -> None:
        """Write a dict/list as JSON."""
        self.write(path, json.dumps(data, indent=2, default=str))


class _LocalBackend:
    """Local filesystem backend for development."""

    def __init__(self, base_path: str) -> None:
        self.base = Path(base_path)
        self.base.mkdir(parents=True, exist_ok=True)

    def read(self, path: str) -> str | None:
        fp = self.base / path
        if not fp.exists():
            return None
        return fp.read_text(encoding="utf-8")

    def write(self, path: str, content: str) -> None:
        fp = self.base / path
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.write_text(content, encoding="utf-8")

    def list_files(self, prefix: str = "") -> list[str]:
        target = self.base / prefix
        if not target.exists():
            return []
        results = []
        for p in target.rglob("*"):
            if p.is_file():
                results.append(str(p.relative_to(self.base)))
        return results


class _BlobBackend:
    """Azure Blob Storage backend."""

    def __init__(self, account_name: str, container_name: str) -> None:
        from azure.identity import DefaultAzureCredential
        from azure.storage.blob import BlobServiceClient

        credential = DefaultAzureCredential()
        self.client = BlobServiceClient(
            account_url=f"https://{account_name}.blob.core.windows.net",
            credential=credential,
        )
        self.container_name = container_name
        # Ensure container exists
        try:
            self.client.create_container(container_name)
        except Exception:
            pass  # Already exists

    def read(self, path: str) -> str | None:
        try:
            blob = self.client.get_blob_client(self.container_name, path)
            return blob.download_blob().readall().decode("utf-8")
        except Exception:
            return None

    def write(self, path: str, content: str) -> None:
        blob = self.client.get_blob_client(self.container_name, path)
        blob.upload_blob(content.encode("utf-8"), overwrite=True)

    def list_files(self, prefix: str = "") -> list[str]:
        container = self.client.get_container_client(self.container_name)
        return [
            b.name
            for b in container.list_blobs(name_starts_with=prefix or None)
        ]
