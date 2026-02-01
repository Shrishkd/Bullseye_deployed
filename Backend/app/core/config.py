# app/core/config.py

import os
from pydantic_settings import BaseSettings


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "bullseye.db")


class Settings(BaseSettings):
    PROJECT_NAME: str = "Bullseye Backend"

    # =====================
    # DATABASE (stable path for Render)
    # =====================
    DATABASE_URL: str = f"sqlite+aiosqlite:///{DB_PATH}"

    # =====================
    # AUTH / JWT
    # =====================
    SECRET_KEY: str = "dev-secret-key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # =====================
    # AI / ML
    # =====================
    GEMINI_API_KEY: str | None = None

    # =====================
    # UPSTOX
    # =====================
    UPSTOX_API_KEY: str | None = None
    UPSTOX_API_SECRET: str | None = None
    UPSTOX_REDIRECT_URI: str | None = None

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
