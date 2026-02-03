from __future__ import annotations

from datetime import datetime
from typing import Any

import requests

from swiggy_zomato_sync.config import ERPNextConfig


class ERPNextClient:
    def __init__(self, config: ERPNextConfig) -> None:
        self.config = config

    def create_pos_invoice(self, payload: dict[str, Any]) -> dict[str, Any]:
        url = f"{self.config.base_url}/api/resource/POS%20Invoice"
        headers = {
            "Authorization": f"token {self.config.api_key}:{self.config.api_secret}",
            "Content-Type": "application/json",
        }
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()

    def build_invoice_payload(self, order: dict[str, Any]) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "company": self.config.company,
            "customer": self.config.customer_default,
            "pos_profile": self.config.pos_profile,
            "items": [],
            "is_pos": 1,
            "is_paid": 1,
            "payments": [
                {
                    "mode_of_payment": "Online",
                    "amount": order.get("total", 0),
                }
            ],
        }

        for key, value in self.config.field_mapping.items():
            payload[key] = value

        for item in order.get("items", []):
            payload_item = {
                "item_code": item.get("item_code") or self.config.item_default,
                "item_name": item.get("item_name"),
                "qty": item.get("qty", 1),
                "rate": item.get("rate", 0),
                "warehouse": self.config.warehouse,
                "cost_center": self.config.cost_center,
            }
            payload["items"].append(payload_item)

        if self.config.taxes_and_charges:
            payload["taxes_and_charges"] = self.config.taxes_and_charges
        return payload

    @staticmethod
    def format_datetime(value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M:%S")
