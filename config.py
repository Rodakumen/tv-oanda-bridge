
from pydantic_settings import SettingsConfigDict, BaseSettings
from pydantic import SecretStr, field_validator


class Settings(BaseSettings):

    WEBHOOK_PASSPHRASE: SecretStr
    DATABASE_URL: str = "sqlite:///./bridge.db"
    OANDA_TOKEN: SecretStr
    ACCOUNT_ID: str

    ALLOWED_SYMBOLS: set[str] = {"EUR_USD"}
    MAX_ORDER_SIZE:  int = 1000
    TRADING_ENABLED: bool = True

    model_config = SettingsConfigDict(env_file=".env")

    @field_validator("ALLOWED_SYMBOLS")
    @classmethod
    def normalize_symbols(cls, v: set[str]) -> set[str]:
        return {s.strip().upper() for s in v if s.strip()}


settings = Settings()
