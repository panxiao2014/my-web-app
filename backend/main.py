from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from apps.App1.routes import router as app1_router
from apps.App2.routes import router as app2_router
from apps.Zhongkao.routes import router as zhongkao_router
from apps.Zhongkao.zhongkao import init_zhongkao

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🔹 Startup
    await init_zhongkao(app)
    yield
    # 🔹 Shutdown (optional)
    print("Shutting down zhongkao...")


app = FastAPI(lifespan=lifespan)

# Configure CORS to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in production, restrict to your domain
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(app1_router)
app.include_router(app2_router)
app.include_router(zhongkao_router)