from pydantic_settings import BaseSettings
from typing import Optional
from dotenv import load_dotenv
import os
from pathlib import Path

# Load .env file explicitly - resolve path relative to project root
project_root = Path(__file__).parent.parent
env_file = project_root / ".env"
load_dotenv(dotenv_path=env_file)


class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production-use-env-variable")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    API_BASE_URL: str = os.getenv("API_BASE_URL", "http://localhost:8000")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

