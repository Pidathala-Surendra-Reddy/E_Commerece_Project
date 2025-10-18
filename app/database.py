# app/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get DATABASE_URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL not set. Copy .env.example to .env and set it."
    )

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True, future=True)

# Create SessionLocal class for dependency injection
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, future=True
)

# Base class for models
class Base(DeclarativeBase):
    pass

# Dependency to use in FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
