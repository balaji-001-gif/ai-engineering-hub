from __future__ import annotations

import time
from datetime import datetime
from typing import Iterable

from swiggy_zomato_sync.clients.swiggy import SwiggyClient
from swiggy_zomato_sync.clients.zomato import ZomatoClient
from swiggy_zomato_sync.config import AppConfig, ProviderConfig
from swiggy_zomato_sync.erpnext_client import ERPNextClient
from swiggy_zomato_sync.normalizer import normalize_order, order_to_payload
from swiggy_zomato_sync.state import SyncState
from swiggy_zomato_sync.utils import unique_items


class SyncService:
    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.erpnext = ERPNextClient(config.erpnext)
        self.state = SyncState.load(config.sync.state_file)

    def run_forever(self) -> None:
        while True:
            self.run_once()
            self.state.save(self.config.sync.state_file)
            time.sleep(self.config.sync.poll_interval_seconds)

    def run_once(self) -> None:
        if self.config.swiggy.enabled:
            self._sync_provider("swiggy", self.config.swiggy, SwiggyClient(self.config.swiggy))
        if self.config.zomato.enabled:
            self._sync_provider("zomato", self.config.zomato, ZomatoClient(self.config.zomato))

    def _sync_provider(self, name: str, config: ProviderConfig, client: object) -> None:
        since = self.state.get_since(name)
        orders = getattr(client, "fetch_orders")(since)
        normalized = [
            normalize_order(name, raw, config, self.config.items) for raw in orders
        ]
        deduped = unique_items([
            order_to_payload(order) for order in normalized
        ], "order_id")

        if not deduped:
            return

        latest_timestamp = max(
            datetime.fromisoformat(item["created_at"]) for item in deduped
        )

        for payload in deduped:
            invoice_payload = self.erpnext.build_invoice_payload(payload)
            self.erpnext.create_pos_invoice(invoice_payload)

        self.state.set_since(name, latest_timestamp)

    @staticmethod
    def summarize_orders(orders: Iterable[dict]) -> str:
        count = len(list(orders))
        return f"Synced {count} orders"
