# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Load .env file
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
    DATABASE_URL: str

settings = Settings()