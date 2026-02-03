# Swiggy + Zomato → ERPNext POS Sync

This service polls Swiggy and Zomato order APIs, normalizes order data, and
creates ERPNext **POS Invoice** documents for online delivery orders.

> ⚠️ You must supply the API endpoints, credentials, and mapping details that
> match your Swiggy/Zomato integration. These APIs are private/partner-only and
> typically require whitelisting.

## Features
- Periodic polling with a state file to avoid duplicate invoices.
- Normalized order payloads for ERPNext POS Invoices.
- Configurable endpoints, headers, and field mappings.
- Works with any ERPNext instance that exposes the REST API.

## Quick start

1. **Create a virtualenv and install dependencies**

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. **Copy the sample config and edit it**

```bash
cp config.sample.yaml config.yaml
```

3. **Run the sync loop**

```bash
python -m swiggy_zomato_sync.run_sync --config config.yaml
```

## Configuration

Edit `config.yaml` to set:

- API base URLs and authentication for Swiggy/Zomato
- ERPNext base URL and API key/secret
- Polling interval and order-to-item mapping

See `config.sample.yaml` for all options.

## Notes
- This implementation provides a robust framework, but the exact Swiggy/Zomato
  API field names vary by partner integration. Update the `field_mapping` and
  `order_path` values to match your payloads.
- ERPNext POS Invoice API docs: `POST /api/resource/POS%20Invoice`.
