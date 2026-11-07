# tests/test_webhook.py
import pytest
from fastapi.testclient import TestClient

from main import app
from config import settings

client = TestClient(app)
PASSPHRASE = settings.WEBHOOK_PASSPHRASE.get_secret_value()

def valid_payload():
    return {
        "passphrase": PASSPHRASE,
        "action": "buy",
        "symbol": "EUR_USD",
        "size": 1000,
        "alert_id": "test-1",
    }

def test_valid_alert_returns_200():
    response = client.post("/webhook/tradingview", json=valid_payload())

    assert response.status_code == 200, response.text
    assert response.json() == {"status": "received"}

def test_wrong_passphrase_returns_401():
    payload = valid_payload()
    payload["passphrase"] = "Banana"
    response = client.post("/webhook/tradingview",json=payload)

    assert response.status_code == 401, response.text

def test_missing_alert_id_returns_422():
    payload = valid_payload()
    del payload["alert_id"]
    response = client.post("/webhook/tradingview", json=payload)

    assert response.status_code == 422, response.text

@pytest.mark.parametrize("field, value", [
    ("action", "banana"),
    ("size", 0),
    ("size", -5),
])
def test_invalid_fields_return_422(field, value):
    payload = valid_payload()
    payload[field] = value
    response = client.post("/webhook/tradingview", json=payload)

    assert response.status_code == 422, response.text
