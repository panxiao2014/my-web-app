"""
Common utilities for user database operations.
This module contains shared functions used across user-related database operations.
"""

import os
from pathlib import Path
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def read_postgres_password() -> str:
    """
    Read PostgreSQL password from environment variable or file.
    
    Returns:
        str: The PostgreSQL password
        
    Raises:
        RuntimeError: If password is not found in environment variable or file
    """
    # First try to get from environment variable (for production/CI)
    password = os.getenv("POSTGRES_PASSWORD")
    if password:
        return password
    
    # Fallback to file for local development
    tokens_path = Path(__file__).resolve().parent.parent.parent / "tokens" / "postgresql.txt"
    try:
        return tokens_path.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        raise RuntimeError(f"PostgreSQL password not found in environment variable POSTGRES_PASSWORD or file at: {tokens_path}")


def init_database_session(app: FastAPI):
    """
    Initialize database session for the application.
    
    Args:
        app: FastAPI application instance
    """
    try:
        password = read_postgres_password()
        database_url = f"postgresql+psycopg2://postgres:{password}@localhost:5432/userdb"
        engine = create_engine(database_url, pool_pre_ping=True)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        app.state.db_engine = engine
        app.state.db_session_factory = SessionLocal
    except Exception as e:
        # For testing environments, use SQLite in-memory database
        if "POSTGRES_PASSWORD" not in os.environ:
            database_url = "sqlite:///:memory:"
            engine = create_engine(database_url)
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            
            app.state.db_engine = engine
            app.state.db_session_factory = SessionLocal
        else:
            raise e
