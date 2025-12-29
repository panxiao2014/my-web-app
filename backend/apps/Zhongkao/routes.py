from fastapi import APIRouter
from apps.Zhongkao.logic import handle_genScore

router = APIRouter(prefix="/api/zhongkao", tags=["Zhongkao"])

# Zhongkao routes will go here
@router.get("/genScore")
async def generate_scores():
    """
    Generate random scores for all courses
    TODO: Implement actual score generation logic
    """
    return await handle_genScore()