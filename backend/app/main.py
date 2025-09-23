from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.config import TEST_PING
from app.users.userdb_requets import router as userdb_router
from app.users.utils import init_database_session, seed_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        init_database_session(app)
    except Exception as e:
        print(f"❌ Failed to initialize database session: {e}")
        raise
    seed_database()
    try:
        yield
    finally:
        if hasattr(app.state, 'db_engine'):
            app.state.db_engine.dispose()

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
