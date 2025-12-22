from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apps.App1.routes import router as app1_router
from apps.App2.routes import router as app2_router

app = FastAPI()

# Configure CORS to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(app1_router)
app.include_router(app2_router)