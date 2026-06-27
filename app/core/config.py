from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.paths import PROJECT_DIR


class Settings(BaseSettings):
    # 应用基础配置
    app_name: str = "FastAPI Project"
    debug: bool = True

    # JWT 配置
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 15

    # 数据库配置
    database_url: str = "sqlite:///./data/database.db"

    # AI 配置
    openai_api_key: str | None = None

    model_config = SettingsConfigDict(
        env_file=PROJECT_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()