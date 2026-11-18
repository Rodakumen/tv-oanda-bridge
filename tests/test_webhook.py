# tests/test_webhook.py
import pytest

from config import settings
from bridge.schemas import AlertPayload

PASSPHRASE = settings.WEBHOOK_PASSPHRASE.get_secret_value()

def valid_payload():
    return {
        "passphrase": PASSPHRASE,
        "action": "buy",
        "symbol": "EUR_USD",
        "size": 1000,
        "alert_id": "test-1",
    }

def test_valid_alert_returns_200(client):
    response = client.post("/webhook/tradingview", json=valid_payload())

    assert response.status_code == 200, response.text
    assert response.json() == {"status": "received"}

def test_wrong_passphrase_returns_401(client):
    payload = valid_payload()
    payload["passphrase"] = "Banana"
    response = client.post("/webhook/tradingview",json=payload)

    assert response.status_code == 401, response.text

def test_missing_alert_id_returns_422(client):
    payload = valid_payload()
    del payload["alert_id"]
    response = client.post("/webhook/tradingview", json=payload)

    assert response.status_code == 422, response.text

@pytest.mark.parametrize("field, value", [
    ("action", "banana"),
    ("size", 0),
    ("size", -5),
    ("symbol","   ")
])
def test_invalid_fields_return_422(client, field, value):
    payload = valid_payload()
    payload[field] = value
    response = client.post("/webhook/tradingview", json=payload)

    assert response.status_code == 422, response.text

def test_first_alert_returns_received(client):
    response = client.post("/webhook/tradingview", json=valid_payload())

    assert response.status_code == 200, response.text
    assert response.json() == {"status": "received"}

def test_same_alert_twice_returns_received_then_duplicate(client):
    payload = valid_payload()

    first = client.post("/webhook/tradingview", json=payload)
    second = client.post("/webhook/tradingview", json=payload)

    assert first.status_code == 200, first.text
    assert first.json() == {"status": "received"}
    assert second.status_code == 200, second.text   # duplicate is not an error
    assert second.json() == {"status": "duplicate"}

def test_symbol_is_normalized():
    payload = valid_payload()
    payload["symbol"] = " eur_usd "
    assert AlertPayload(**payload).symbol == "EUR_USD"