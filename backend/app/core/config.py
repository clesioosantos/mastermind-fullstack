from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Mastermind API"
    APP_ENV: str = "development"

    DATABASE_URL: str

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 1440

    CORS_ALLOWED_ORIGINS: str = "http://localhost:4200"

    model_config = ConfigDict(env_file=".env")


settings = Settings()
