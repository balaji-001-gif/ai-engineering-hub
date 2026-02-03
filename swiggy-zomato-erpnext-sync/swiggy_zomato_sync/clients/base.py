from __future__ import annotations

from typing import Any

import requests

from swiggy_zomato_sync.config import ProviderConfig


class ProviderClient:
    def __init__(self, config: ProviderConfig) -> None:
        self.config = config

    def fetch_orders(self, since: str | None = None) -> list[dict[str, Any]]:
        params = dict(self.config.params)
        if since:
            params["since"] = since

        url = f"{self.config.base_url}{self.config.orders_endpoint}"
        headers = {self.config.auth_header: self.config.auth_token}
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        payload = response.json()
        return self._extract_orders(payload)

    def _extract_orders(self, payload: dict[str, Any]) -> list[dict[str, Any]]:
        parts = self.config.order_path.split(".")
        current: Any = payload
        for part in parts:
            if isinstance(current, dict):
                current = current.get(part)
            else:
                current = None
                break
        if current is None:
            return []
        if isinstance(current, list):
            return current
        raise ValueError("Order path did not resolve to a list")
