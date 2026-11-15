# TradingView → Oanda Bridge

A small FastAPI service that receives TradingView webhook alerts, validates them,
and (in later steps) places orders at Oanda safely: no duplicate orders, no silent failures.

## Status

- [x] Webhook endpoint with schema validation and constant-time passphrase check
- [x] Automated tests (pytest)
- [x] Alert log with idempotency (unique `alert_id`)
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
| 200 `{"status": "received"}` | New alert, logged |
| 200 `{"status": "duplicate"}` | Same `alert_id` already seen, nothing done |
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
- **Duplicates return 200.** A duplicate is not a failure: the alert was already
  handled. An error code would make retrying senders resend forever, so the body says
  `{"status": "duplicate"}` and the log shows what happened.
- **Uniqueness is enforced by the database.** `alert_id` has a unique constraint and
  the service inserts first and catches the error, instead of checking first. Two
  identical alerts arriving at the same moment can't both succeed.
- **The passphrase is never stored.** It is checked in the router and not passed to
  the service, repository or log.