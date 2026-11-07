
from pydantic_settings import SettingsConfigDict, BaseSettings
from pydantic import SecretStr


class Settings(BaseSettings):

    WEBHOOK_PASSPHRASE: SecretStr
    OANDA_TOKEN: SecretStr
    ACCOUNT_ID: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
