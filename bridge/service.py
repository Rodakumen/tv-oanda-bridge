# bridge/service.py
from bridge.repository import AlertRepository
from bridge.schemas import AlertPayload


class AlertService:
    def __init__(self, repo: AlertRepository):
        self.repo = repo

    def handle_alert(self, payload: AlertPayload) -> str:
        """Return "received" for a new alert, "duplicate" for a repeat."""
        is_new = self.repo.record_alert(
            alert_id=payload.alert_id,
            action=payload.action.value,
            symbol=payload.symbol,
            size=payload.size,
        )

        return "received" if is_new else "duplicate"