from __future__ import annotations

import argparse

from swiggy_zomato_sync.config import load_config
from swiggy_zomato_sync.sync import SyncService


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync Swiggy/Zomato orders into ERPNext POS invoices")
    parser.add_argument("--config", default="config.yaml", help="Path to config.yaml")
    parser.add_argument("--once", action="store_true", help="Run a single sync pass and exit")
    args = parser.parse_args()

    config = load_config(args.config)
    service = SyncService(config)

    if args.once:
        service.run_once()
    else:
        service.run_forever()


if __name__ == "__main__":
    main()
