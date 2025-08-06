from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    APP_NAME: str = "DB-Learn"
    DESCRIPTION: str = "Interactive database learning platform"

    #Подключение к базе данных
    #DATABASE_URL: str = "sqlite:///./db.sqlite3"
    DATABASE_URL: str = "postgresql://postgres:postgresql@localhost:5432/dblearn"

    # Content paths
    CONTENT_DIR: str = "content"

    # Sandbox settings
    SQL_TIMEOUT_SECONDS: float = 5.0
    SQL_MAX_ROWS: int = 1000

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()