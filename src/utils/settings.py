
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Get project root directory
BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    DATABASE_URL: str
    SECRETE_KEY: str
    ALGORITHM:str
    EXP_TIME : int


settings = Settings()
