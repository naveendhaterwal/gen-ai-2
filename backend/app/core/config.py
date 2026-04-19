"""
Configuration settings for the Credit Risk AI Backend.
Load environment variables and manage app-wide settings.
"""

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict
from pydantic_settings import PydanticBaseSettingsSource
from typing import Optional
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
ENV_FILE_PATH = BASE_DIR / ".env"


class Settings(BaseSettings):
    """
    All app settings in one place.
    Read from environment variables with defaults provided.
    """
    
    # App Info
    APP_NAME: str = "Credit Risk AI Backend"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # API Keys & External Services
    GROQ_API_KEY: Optional[str] = None
    GROQ_MODEL: str = "llama-3.1-8b-instant"
    QDRANT_API_KEY: Optional[str] = None
    
    # Qdrant Vector DB
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_COLLECTION: str = "lending_policies"
    
    # ML Model Paths
    ML_MODEL_PATH: str = "./models/logistic_model.pkl"
    FEATURE_COLUMNS_PATH: str = "./models/feature_columns.pkl"

    # Runtime behavior
    # When enabled, backend will fail requests instead of returning deterministic/mock fallback outputs.
    STRICT_NO_FALLBACKS: bool = True
    
    # CORS (comma-separated in .env)
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:3001"

    def get_cors_origins(self) -> list[str]:
        """Return CORS origins as a clean list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
    
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE_PATH),
        case_sensitive=True,
        extra="ignore",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ):
        """Read .env before shell env vars for project-local consistency."""
        return (
            init_settings,
            dotenv_settings,
            env_settings,
            file_secret_settings,
        )


# Create single instance to use across app
settings = Settings()
