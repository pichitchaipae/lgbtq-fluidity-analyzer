"""Application configuration and settings."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "LGBTQ+ Sexual Fluidity Analysis API"
    api_v1_str: str = "/api/v1"
    cors_allow_origins: list[str] = ["*"]
    
    # AI Provider settings
    ai_provider: str = "gemini"  # Options: 'gemini' or 'openai'
    gemini_api_key: str = ""  # Google Gemini API key (free forever)
    openai_api_key: str = ""  # OpenAI API key (optional fallback)

    class Config:
        env_file = ".env"
        case_sensitive = False


def get_settings() -> Settings:
    return Settings()
