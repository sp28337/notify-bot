from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseModel):
    host: str = ""
    port: int = 0
    token: str = ""
    target_chat_id: int = 0
    webhook_url: str = ""
    webhook_secret: str = ""


class Settings(BaseSettings):
    env: str = ""
    pythonunbuffered: int = 1

    bot: BotSettings = BotSettings()

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=".env",
        env_nested_delimiter="__",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
