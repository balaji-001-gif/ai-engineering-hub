from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class OrderItem:
    item_code: str
    item_name: str
    qty: float
    rate: float
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass
class Order:
    source: str
    order_id: str
    created_at: datetime
    customer_name: str | None
    customer_phone: str | None
    total: float
    items: list[OrderItem]
    raw: dict[str, Any] = field(default_factory=dict)
