from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Finance Dashboard API"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SECRET_KEY: str = "a_very_secret_key_please_change_in_production"
    DATABASE_URL: str = "sqlite:///./finance.db"

settings = Settings()
