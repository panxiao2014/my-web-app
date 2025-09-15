from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from .userdb_ops import choose_ramdon_user


router = APIRouter()


def get_db(request: Request) -> Session:
    """Dependency to get database session"""
    return request.app.state.db_session_factory()


@router.post("/addUser")
async def add_user():
  return "addUser received"


@router.get("/ramdonUser")
async def ramdon_user(db: Session = Depends(get_db)):
    user = choose_ramdon_user(db)
    if user is None:
        raise HTTPException(status_code=404, detail="No users found in database")
    return user


