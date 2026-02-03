from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class SyncState:
    providers: dict[str, str] = field(default_factory=dict)

    @classmethod
    def load(cls, path: str | Path) -> "SyncState":
        file_path = Path(path)
        if not file_path.exists():
            return cls()
        with file_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        providers = data.get("providers", {}) if isinstance(data, dict) else {}
        return cls(providers=providers)

    def save(self, path: str | Path) -> None:
        file_path = Path(path)
        payload = {"providers": self.providers}
        with file_path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)

    def get_since(self, provider: str) -> str | None:
        return self.providers.get(provider)

    def set_since(self, provider: str, value: datetime) -> None:
        self.providers[provider] = value.isoformat()
