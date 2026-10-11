from dotenv import load_dotenv
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class _Config(BaseSettings):
    PORT_APP: int = 8000

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

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

    @field_validator("JWT_SECRET_KEY")
    @classmethod
    def validate_jwt_secret(cls, v: str) -> str:
        if not v or len(v.strip()) < 32:
            raise ValueError(
                "La variable JWT_SECRET_KEY es obligatoria y debe tener al menos 32 caracteres para garantizar seguridad."
            )
        return v



load_dotenv()

CONFIG = _Config()