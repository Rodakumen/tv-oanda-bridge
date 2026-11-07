
import hmac

from fastapi import APIRouter, HTTPException

from bridge.schemas import AlertPayload
from config import settings

router = APIRouter()

@router.post("/webhook/tradingview")
async def tradingview_webhook(payload: AlertPayload):
    expected = settings.WEBHOOK_PASSPHRASE.get_secret_value().encode()
    received = payload.passphrase.encode()

    if not hmac.compare_digest(expected, received):
        raise HTTPException(status_code=401, detail="Invalid passphrase")

    return {"status": "received"}
