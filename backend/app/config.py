from typing import Optional

from pydantic_settings import BaseSettings


class SettingsConfig(BaseSettings):
    database_url: str = "postgresql+psycopg://localhost/polymarket"
    openai_api_key: Optional[str] = None
    alpha_vantage_api_key: Optional[str] = None
    gmail_smtp_user: Optional[str] = None
    gmail_smtp_password: Optional[str] = None


def get_settings() -> SettingsConfig:
    return SettingsConfig()
