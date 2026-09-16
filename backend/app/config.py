import os
from pydantic import BaseModel

class Settings(BaseModel):
    APP_NAME: str = "VoltRoute Backend"
    VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./charging_stations.db")
    OSRM_BASE_URL: str = os.getenv("OSRM_BASE_URL", "https://router.project-osrm.org")
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "https://*.vercel.app",
        "*"
    ]

settings = Settings()
