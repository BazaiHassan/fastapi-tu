from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).parent.parent.parent

class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str
    API_VERSION: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: float
    REFRESH_TOKEN_EXPIRE_DAYS: float
    REDIS_URL: str

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8"
    )

settings = Settings()