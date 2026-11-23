# bridge/repository.py
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from bridge.models import AlertLog, AlertStatus


class AlertRepository:
    def __init__(self, db: Session):
        self.db = db

    def record_alert(self, alert_id: str, action: str, symbol: str, size: int) -> bool:
        """Insert a new alert. True if new, False if alert_id already existed."""
        entry = AlertLog(alert_id=alert_id,action=action,symbol=symbol,size=size)       # build the row
        self.db.add(entry)
        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            return False
        return True

    def get_by_alert_id(self, alert_id: str) -> AlertLog | None:
        stmt = select(AlertLog).where(AlertLog.alert_id == alert_id)
        return self.db.scalars(stmt).first()

    def update_status(self, alert_id: str, status: AlertStatus, reason: str | None = None) -> None:
        row = self.get_by_alert_id(alert_id)

        if row is None:
            raise ValueError(f"Unknown alert_id: {alert_id!r}")

        row.status = status
        row.reason = reason
        self.db.commit()