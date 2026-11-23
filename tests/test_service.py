# tests/test_service.py
from bridge.models import AlertStatus, AlertLog
from bridge.repository import AlertRepository
from bridge.schemas import AlertPayload
from bridge.service import AlertService
from sqlalchemy import select


def make_service(db, enabled=True):
    return AlertService(AlertRepository(db), {"EUR_USD"}, 1000, enabled)


def make_payload(**overrides):
    data = {
        "passphrase": "x",
        "action": "buy",
        "symbol": "EUR_USD",
        "size": 500,
        "alert_id": "a1",
    }
    data.update(overrides)
    return AlertPayload(**data)


def test_normal_alert_is_received(db):
    service = make_service(db)
    assert service.handle_alert(make_payload()) == "received"


def test_duplicate_alert(db):
    service = make_service(db)
    service.handle_alert(make_payload())
    assert service.handle_alert(make_payload()) == "duplicate"


def test_oversized_alert_is_rejected_and_logged(db):
    service = make_service(db)
    result = service.handle_alert(make_payload(size=5000))
    assert result == "rejected"

    repo = AlertRepository(db)
    entry = repo.get_by_alert_id("a1")
    assert entry.status == AlertStatus.REJECTED
    assert entry.reason == "size_exceeds_max"

    reason = db.scalar(select(AlertLog.reason).where(AlertLog.alert_id == "a1"))
    assert reason == "size_exceeds_max"


def test_kill_switch_rejects_buy_but_not_close(db):
    service = make_service(db, enabled=False)

    buy = service.handle_alert(make_payload(action="buy", alert_id="a1"))
    close = service.handle_alert(make_payload(action="close", alert_id="a2"))

    assert buy == "rejected"
    assert close == "received"

    reason = db.scalar(select(AlertLog.reason).where(AlertLog.alert_id == "a1"))
    assert reason == "kill_switch"