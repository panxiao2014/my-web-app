"""
Common utilities for user database operations.
This module contains shared functions used across user-related database operations.
"""

import os
import socket
from pathlib import Path
from fastapi import FastAPI
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


def get_db_host() -> str:
    # Check if we're running in GitHub Actions
    if os.getenv("GITHUB_ACTIONS"):
        # In GitHub Actions, check if we're running inside a Docker container
        # by looking for the /.dockerenv file or checking if we can resolve host.docker.internal
        try:
            # If we can resolve host.docker.internal, we're likely in a container
            socket.gethostbyname("host.docker.internal")
            return "postgres"  # Use mapped hostname for Docker containers
        except socket.error:
            # We're running directly on the GitHub runner, not in a container
            return "localhost"  # PostgreSQL service is accessible via localhost
    
    # Check if we're running in Docker (local development)
    try:
        socket.gethostbyname("host.docker.internal")
        return "host.docker.internal"
    except socket.error:
        return "localhost"
    

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
    db_host = get_db_host()

    try:
        password = read_postgres_password()
        database_url = f"postgresql+psycopg2://postgres:{password}@{db_host}:5432/userdb"
        engine = create_engine(database_url, pool_pre_ping=True)
        # Probe connectivity early to fail fast
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    except Exception as exc:
        message = "Failed to initialize database session to host '{host}': {err}".format(
            host=db_host, err=str(exc)
        )
        raise RuntimeError(message) from exc

    app.state.db_engine = engine
    app.state.db_session_factory = SessionLocal
