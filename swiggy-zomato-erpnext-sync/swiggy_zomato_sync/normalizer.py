from __future__ import annotations

from datetime import datetime
from typing import Any

from swiggy_zomato_sync.config import ItemsConfig, ProviderConfig
from swiggy_zomato_sync.models import Order, OrderItem
from swiggy_zomato_sync.utils import coerce_datetime, get_by_path


def normalize_order(provider: str, raw: dict[str, Any], config: ProviderConfig, items: ItemsConfig) -> Order:
    field_map = config.field_mapping
    order_id = get_by_path(raw, field_map.get("id", "id")) or ""
    created_raw = get_by_path(raw, field_map.get("created_at", "created_at"))
    created_at = coerce_datetime(created_raw) or datetime.utcnow()

    customer_name = get_by_path(raw, field_map.get("customer_name", "customer_name"))
    customer_phone = get_by_path(raw, field_map.get("customer_phone", "customer_phone"))
    total = float(get_by_path(raw, field_map.get("total", "total")) or 0)

    items_raw = get_by_path(raw, field_map.get("items", "items")) or []
    item_mapping = items.field_mapping

    normalized_items: list[OrderItem] = []
    for item in items_raw:
        item_code = get_by_path(item, item_mapping.get("item_code", "item_code")) or ""
        item_name = get_by_path(item, item_mapping.get("item_name", "item_name")) or item_code
        qty = float(get_by_path(item, item_mapping.get("qty", "qty")) or 1)
        rate = float(get_by_path(item, item_mapping.get("rate", "rate")) or 0)
        normalized_items.append(
            OrderItem(
                item_code=item_code,
                item_name=item_name,
                qty=qty,
                rate=rate,
                raw=item,
            )
        )

    return Order(
        source=provider,
        order_id=str(order_id),
        created_at=created_at,
        customer_name=customer_name,
        customer_phone=customer_phone,
        total=total,
        items=normalized_items,
        raw=raw,
    )


def order_to_payload(order: Order) -> dict[str, Any]:
    return {
        "source": order.source,
        "order_id": order.order_id,
        "created_at": order.created_at.isoformat(),
        "customer_name": order.customer_name,
        "customer_phone": order.customer_phone,
        "total": order.total,
        "items": [
            {
                "item_code": item.item_code,
                "item_name": item.item_name,
                "qty": item.qty,
                "rate": item.rate,
            }
            for item in order.items
        ],
    }
