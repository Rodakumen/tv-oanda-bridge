
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

class Action(str, Enum):
    BUY = "buy"
    SELL = "sell"
    CLOSE = "close"

class AlertPayload(BaseModel):
    passphrase: str
    action: Action
    symbol: str
    size: int = Field(gt=0)  # constraint: greater than 0
    alert_id: str
