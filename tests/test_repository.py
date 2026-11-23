import pytest
from bridge import models  # noqa: F401  (registers the table with Base)
from bridge.repository import AlertRepository
from sqlalchemy import select
from bridge.models import AlertLog, AlertStatus





def test_first_insert_returns_true(db):
    repo = AlertRepository(db)
    assert repo.record_alert("a1", "buy", "EUR_USD", 1000) is True

def test_duplicate_alert_id_returns_false_and_keeps_one_row(db):
    repo = AlertRepository(db)
    repo.record_alert("a1", "buy", "EUR_USD", 1000)
    assert repo.record_alert("a1", "buy", "EUR_USD", 1000) is False

    rows = db.scalars(select(AlertLog)).all()
    assert len(rows) == 1


def test_new_alert_has_default_status_and_timestamp(db):
    repo = AlertRepository(db)
    repo.record_alert("a1", "buy", "EUR_USD", 1000)

    entry = repo.get_by_alert_id("a1")

    assert entry is not None
    assert entry.status == AlertStatus.RECEIVED
    assert entry.created_at is not None

def test_status_update_works(db):
    repo = AlertRepository(db)
    repo.record_alert("a1", "buy", "EUR_USD", 1000)

    repo.update_status("a1", AlertStatus.REJECTED, "size_exceeds_max")

    entry = repo.get_by_alert_id("a1")

    #reason = db.scalar(select(AlertLog.reason).where(AlertLog.alert_id == "a1"))
    #assert reason == "size_exceeds_max"
    assert entry.status == AlertStatus.REJECTED
    assert entry.reason == "size_exceeds_max"

def test_update_unknown_alert_raises(db):
    repo = AlertRepository(db)
    with pytest.raises(ValueError):
        repo.update_status("missing", AlertStatus.FAILED)

