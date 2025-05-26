__all__ = ("settings", "alembic_config")

from pathlib import Path

from alembic.config import Config
from dotenv import load_dotenv
from pydantic import PostgresDsn, SecretStr
from pydantic_settings import BaseSettings


load_dotenv(".env")


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent.parent
    DEBUG: bool = False
    DB_URL: PostgresDsn
    API_KEY_V1: SecretStr
    API_KEY_V1_NAME: str
    API_KEY_V1_SCOPE: str


settings = Settings()
alembic_config = Config(settings.BASE_DIR / "alembic.ini")
