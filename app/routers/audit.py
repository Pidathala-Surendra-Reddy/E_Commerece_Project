# app/routers/auth.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.get("/test")
def test_auth():
    return {"message": "Auth router is working"}
