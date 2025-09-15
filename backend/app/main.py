import os
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.config import TEST_PING
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.users.userdb_requets import router as userdb_router

def _read_postgres_password() -> str:
    tokens_path = Path(__file__).resolve().parent.parent / "tokens" / "postgresql.txt"
    try:
        return tokens_path.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        raise RuntimeError(f"PostgreSQL password file not found at: {tokens_path}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    password = _read_postgres_password()
    database_url = f"postgresql+psycopg2://postgre:{password}@localhost:5432/postgres"
    engine = create_engine(database_url, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    app.state.db_engine = engine
    app.state.db_session_factory = SessionLocal
    try:
        yield
    finally:
        engine.dispose()


app = FastAPI(title="my-web-app API", lifespan=lifespan)

# Allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in production, restrict to your domain
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
async def ping():
    return {"message": TEST_PING}

app.include_router(userdb_router)
