# bridge/service.py
from bridge.models import AlertStatus
from bridge.repository import AlertRepository
from bridge.schemas import AlertPayload
from risk.rules import check_rules


class AlertService:
    def __init__(self, repo: AlertRepository, allowed_symbols: set[str], max_size: int, trading_enabled: bool):
        self.repo = repo
        self.allowed_symbols = allowed_symbols
        self.max_size = max_size
        self.trading_enabled = trading_enabled

    def handle_alert(self, payload: AlertPayload) -> str:
        """Return "duplicate", "rejected" or "received"."""
        is_new = self.repo.record_alert(
            alert_id=payload.alert_id,
            action=payload.action.value,
            symbol=payload.symbol,
            size=payload.size,
        )
        if not is_new:
            return "duplicate"

        reason = check_rules(
            payload.action.value,
            payload.symbol,
            payload.size,
            self.allowed_symbols,
            self.max_size,
            self.trading_enabled,
        )
        if reason is not None:
            self.repo.update_status(payload.alert_id, AlertStatus.REJECTED, reason)
            return "rejected"

        return "received"