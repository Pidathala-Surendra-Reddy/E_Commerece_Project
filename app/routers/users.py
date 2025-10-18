# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import UserCreate, Token
from app.models import User
from app.database import get_db
from passlib.context import CryptContext
from jose import jwt, JWTError
import os

router = APIRouter(prefix="/user", tags=["User"])

# ---------------- Password hashing ----------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ---------------- JWT ----------------
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_secret_key")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

def create_access_token(user_id: int):
    payload = {"user_id": user_id}
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

# ---------------- Register ----------------
@router.post("/register", response_model=Token)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=hash_password(user.password),
        phone=user.phone,
        address=user.address
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token(new_user.user_id)
    return {"access_token": token, "token_type": "bearer"}

# ---------------- Login ----------------
@router.post("/login", response_model=Token)
def login_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    token = create_access_token(db_user.user_id)
    return {"access_token": token, "token_type": "bearer"}
