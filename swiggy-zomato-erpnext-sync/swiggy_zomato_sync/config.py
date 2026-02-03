from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError("Config root must be a mapping")
    return data


@dataclass
class ProviderConfig:
    enabled: bool = True
    base_url: str = ""
    orders_endpoint: str = ""
    auth_header: str = ""
    auth_token: str = ""
    params: dict[str, Any] = field(default_factory=dict)
    order_path: str = "data.orders"
    field_mapping: dict[str, str] = field(default_factory=dict)


@dataclass
class ERPNextConfig:
    base_url: str = ""
    api_key: str = ""
    api_secret: str = ""
    company: str = ""
    customer_default: str = "Online Customer"
    pos_profile: str = "Online POS"
    item_default: str = "Online Item"
    warehouse: str = ""
    cost_center: str = ""
    taxes_and_charges: str = ""
    field_mapping: dict[str, str] = field(default_factory=dict)


@dataclass
class ItemsConfig:
    field_mapping: dict[str, str] = field(default_factory=dict)


@dataclass
class SyncConfig:
    poll_interval_seconds: int = 120
    state_file: str = ".sync_state.json"


@dataclass
class AppConfig:
    sync: SyncConfig
    swiggy: ProviderConfig
    zomato: ProviderConfig
    erpnext: ERPNextConfig
    items: ItemsConfig


def load_config(path: str | Path) -> AppConfig:
    data = _load_yaml(Path(path))

    sync = SyncConfig(**data.get("sync", {}))
    swiggy = ProviderConfig(**data.get("swiggy", {}))
    zomato = ProviderConfig(**data.get("zomato", {}))
    erpnext = ERPNextConfig(**data.get("erpnext", {}))
    items = ItemsConfig(**data.get("items", {}))

    return AppConfig(sync=sync, swiggy=swiggy, zomato=zomato, erpnext=erpnext, items=items)
