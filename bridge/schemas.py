
from enum import Enum

from pydantic import BaseModel, Field, field_validator


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

    @field_validator("symbol")
    @classmethod
    def normalize_symbol(cls, v: str) -> str:
        v = v.strip().upper()
        if not v:
            raise ValueError("symbol must not be empty")
        return v
