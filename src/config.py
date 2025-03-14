from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", extra="ignore")

    TELEGRAM_BOT_API_TOKEN: str

settings = Settings()  # type: ignore
