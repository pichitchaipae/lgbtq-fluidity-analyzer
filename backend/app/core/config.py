"""Application configuration and settings."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "LGBTQ+ Sexual Fluidity Analysis API"
    api_v1_str: str = "/api/v1"
    cors_allow_origins: list[str] = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = False


def get_settings() -> Settings:
    return Settings()
