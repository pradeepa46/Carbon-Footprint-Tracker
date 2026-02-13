from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import StaticPool
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    """Application settings from environment variables."""
    DATABASE_URL: str = "sqlite:///./test.db"
    JWT_SECRET_KEY: str = "test-secret-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    FRONTEND_URL: str = "http://localhost:5173"

    class Config:
        env_file = ".env"

settings = Settings()

# Create engine based on database URL
if "sqlite" in settings.DATABASE_URL:
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    engine = create_engine(
        settings.DATABASE_URL,
        echo=False,
        future=True,
        pool_pre_ping=True,
    )

def create_db_and_tables():
    """Create database tables."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependency: Get database session."""
    with Session(engine) as session:
        yield session
