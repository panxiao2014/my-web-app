from fastapi import APIRouter
from apps.App1.logic import handle_ping

router = APIRouter(prefix="/api/app1", tags=["App1"])

@router.get("/ping")
async def ping():
    return await handle_ping()