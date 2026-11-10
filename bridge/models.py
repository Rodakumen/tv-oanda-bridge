# bridge/models.py

import enum
from datetime import datetime, timezone

from sqlalchemy import String, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column

from bridge.database import Base

class AlertStatus(str, enum.Enum):
    RECEIVED = "received"
    EXECUTED = "executed"
    FAILED   = "failed"


class AlertLog(Base):
    __tablename__ = "alert_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    alert_id: Mapped[str] = mapped_column(unique=True,nullable=False)
    action:  Mapped[str] = mapped_column(String)
    symbol: Mapped[str] = mapped_column(String)
    size: Mapped[int] = mapped_column()
    status: Mapped[AlertStatus] = mapped_column(
        Enum(AlertStatus), default=AlertStatus.RECEIVED
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )