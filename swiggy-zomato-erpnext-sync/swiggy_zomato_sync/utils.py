from __future__ import annotations

from datetime import datetime
from typing import Any, Iterable


def get_by_path(payload: dict[str, Any], path: str) -> Any:
    current: Any = payload
    for part in path.split("."):
        if current is None:
            return None
        if isinstance(current, dict):
            current = current.get(part)
        else:
            return None
    return current


def coerce_datetime(value: Any) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    for fmt in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(str(value), fmt)
        except ValueError:
            continue
    return None


def unique_items(items: Iterable[dict[str, Any]], key: str) -> list[dict[str, Any]]:
    seen: set[Any] = set()
    result: list[dict[str, Any]] = []
    for item in items:
        value = item.get(key)
        if value in seen:
            continue
        seen.add(value)
        result.append(item)
    return result
