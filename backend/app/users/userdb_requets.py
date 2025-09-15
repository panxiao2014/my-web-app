from fastapi import APIRouter
from .userdb_ops import choose_ramdon_user


router = APIRouter()


@router.post("/addUser")
async def add_user():
  return "addUser received"


@router.get("/ramdonUser")
async def ramdon_user():
  user = choose_ramdon_user()
  return user


