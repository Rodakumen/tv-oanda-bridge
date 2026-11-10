import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from bridge.database import Base
from bridge import models  # noqa: F401  (registers the table with Base)
from bridge.repository import AlertRepository
from sqlalchemy import select
from bridge.models import AlertLog, AlertStatus


@pytest.fixture
def db():
    engine = create_engine("sqlite://")      # in-memory, thrown away after each test
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


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