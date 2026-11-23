import hmac

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from bridge.database import get_db
from bridge.repository import AlertRepository
from bridge.schemas import AlertPayload
from bridge.service import AlertService
from config import settings

router = APIRouter()


def get_repository(db: Session = Depends(get_db)) -> AlertRepository:
    return AlertRepository(db)


def get_service(repo: AlertRepository = Depends(get_repository)) -> AlertService:
    return AlertService(repo,settings.ALLOWED_SYMBOLS,settings.MAX_ORDER_SIZE,settings.TRADING_ENABLED)


@router.post("/webhook/tradingview")
def tradingview_webhook(
    payload: AlertPayload,
    service: AlertService = Depends(get_service),
):
    expected = settings.WEBHOOK_PASSPHRASE.get_secret_value().encode()
    received = payload.passphrase.encode()
    if not hmac.compare_digest(expected, received):
        raise HTTPException(status_code=401, detail="Invalid passphrase")

    result = service.handle_alert(payload)
    return {"status": result}