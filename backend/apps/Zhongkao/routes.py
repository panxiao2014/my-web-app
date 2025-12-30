from fastapi import APIRouter, Request
from apps.Zhongkao.logic import handle_genScore

router = APIRouter(prefix="/api/zhongkao", tags=["Zhongkao"])

# Zhongkao routes will go here
@router.get("/genScore")
async def generate_scores(request: Request):
    """
    Generate random scores for all courses
    TODO: Implement actual score generation logic
    """
    stuSet = request.app.state.stuSet
    return await handle_genScore(stuSet)