from fastapi import APIRouter

router = APIRouter(prefix="/api/zhongkao", tags=["Zhongkao"])

# Zhongkao routes will go here
@router.get("/genScore")
async def generate_scores():
    """
    Generate random scores for all courses
    TODO: Implement actual score generation logic
    """
    # Fake response for now - returns fixed scores
    fake_scores = [100, 95, 88, 60, 45, 50, 16, 12, 16, 12]
    
    return {
        "scores": fake_scores
    }