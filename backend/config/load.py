import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class _Config(BaseSettings):
    PORT_APP: int = 8000

    JWT_SECRET_KEY: str = "" 

    CORS_ALLOW_ORIGINS: list[str] = ["*"]
    CORS_ALLOW_METHODS: list[str] = ["GET", "POST"]
    CORS_ALLOW_HEADERS: list[str] = ["Content-Type"]
    CORS_ALLOW_CREDENTIALS: bool = True

    POSTGRES_USER: str = "root"
    POSTGRES_PASSWORD: str = "root"

    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "cfs-admin"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )



load_dotenv()

CONFIG = _Config()