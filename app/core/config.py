from pydantic_settings import BaseSettings
import secrets
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # JWT settings
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database settings
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 