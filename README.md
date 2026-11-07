# TradingView → Oanda Bridge

A small FastAPI service that receives TradingView webhook alerts, validates them,
and (in later steps) places orders at Oanda safely: no duplicate orders, no silent failures.

## Status

- [x] Webhook endpoint with schema validation and constant-time passphrase check
- [x] Automated tests (pytest)
- [ ] Alert log with idempotency (unique `alert_id`)
- [ ] Oanda client (practice account) and risk rules
- [ ] Background execution, retries, failure notifications
- [ ] Docker + deployment

## Alert format

TradingView sends a POST to `/webhook/tradingview` with a JSON body:

```json
{
  "passphrase": "your-shared-secret",
  "action": "buy",
  "symbol": "EUR_USD",
  "size": 1000,
  "alert_id": "unique-id-per-alert"
}
```

| Field | Rules |
|---|---|
| `passphrase` | Must match `WEBHOOK_PASSPHRASE` in `.env` |
| `action` | Lowercase only: `buy`, `sell` or `close` |
| `symbol` | String, Oanda format (e.g. `EUR_USD`) |
| `size` | Integer, greater than 0 |
| `alert_id` | Required, unique per alert |

## Responses

| Status | Meaning |
|---|---|
| 200 | Alert accepted |
| 401 | Wrong passphrase |
| 422 | Invalid body (bad action, size ≤ 0, missing field) |

## Setup

```powershell
pip install ".[dev]"
copy .env.example .env      # Windows (Mac/Linux: cp .env.example .env)
# then open .env and fill in real values
uvicorn main:app --reload
```

Generate a passphrase with:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Tests

```bash
pytest -v
```

## Design notes

- **Validation at the boundary.** Pydantic rejects malformed alerts before any
  business logic runs, so a bad alert can never become a bad order.
- **Passphrase auth.** TradingView cannot sign requests, so the shared secret is sent
  in the body and compared with `hmac.compare_digest` (constant time).
  It is never logged or returned.
- **Strict action values.** A typo is rejected loudly (422) instead of being
  silently "fixed".
