from pydantic_settings import BaseSettings
from pydantic import computed_field


class Settings(BaseSettings):
    # Database Configuration
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int

    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # Default to 1 hour

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.DB_USER}:"
            f"{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:"
            f"{self.DB_PORT}/"
            f"{self.DB_NAME}"
        )

    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra fields from .env (e.g., PGADMIN_*)


settings = Settings()
