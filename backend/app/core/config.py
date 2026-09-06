from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings

BACKEND_ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "SupportAI"
    APP_VERSION: str = "0.1.0"
    APP_ENV: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://supportai:supportai@localhost:5432/supportai"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # MinIO
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET_DOCUMENTS: str = "documents"
    MINIO_BUCKET_AVATARS: str = "avatars"
    MINIO_BUCKET_EXPORTS: str = "exports"
    MINIO_SECURE: bool = False

    # JWT (secret must come from the environment / .env, never hardcoded)
    JWT_SECRET: str | None = None
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # LLM
    LLM_PROVIDER: str = "ollama"
    LLM_MODEL: str = "qwen2:0.5b"
    LLM_HOST: str = "http://localhost:11434"
    LLM_TIMEOUT_SECONDS: int = 60

    # Embeddings
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    EMBEDDING_DIMENSIONS: int = 384

    # RAG
    RAG_TOP_K: int = 5
    RAG_CHUNK_SIZE: int = 800
    RAG_CHUNK_OVERLAP: int = 100

    # File upload
    MAX_UPLOAD_SIZE_MB: int = 10
    ALLOWED_EXTENSIONS: list[str] = ["pdf", "txt", "docx"]

    # Rate limiting
    RATE_LIMIT_LOGIN_PER_MINUTE: int = 5
    RATE_LIMIT_API_PER_MINUTE: int = 100
    RATE_LIMIT_AI_PER_MINUTE: int = 20

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:5173"]

    # Logging
    LOG_LEVEL: str = "INFO"

    @field_validator("JWT_SECRET")
    @classmethod
    def validate_jwt_secret(cls, v: str | None) -> str:
        if not v:
            raise ValueError(
                "JWT_SECRET must be set: keep secrets in backend/.env (see .env.example), "
                "never hardcode them in source"
            )
        return v

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        if not v.startswith("postgresql"):
            raise ValueError("DATABASE_URL must be a PostgreSQL connection string")
        return v

    @field_validator("ALLOWED_EXTENSIONS")
    @classmethod
    def normalize_extensions(cls, v: list[str]) -> list[str]:
        return [ext.lower().lstrip(".") for ext in v]

    model_config = {
        "env_file": BACKEND_ENV_FILE,
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


settings = Settings()
