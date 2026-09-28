import os
from dataclasses import dataclass

@dataclass
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./event_tracker.db")
    jwt_secret: str = os.getenv("JWT_SECRET", "change-this-local-secret")
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = int(os.getenv("ACCESS_TOKEN_MINUTES", "120"))
    cors_origins: str = os.getenv("CORS_ORIGINS", "http://localhost:5173")
    app_env: str = os.getenv("APP_ENV", "local")

settings = Settings()
