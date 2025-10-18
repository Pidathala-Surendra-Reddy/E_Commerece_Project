from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import AdminCreate, AdminOut, Token
from app.models import Admin
from app.database import get_db
from app.dependencies import get_current_admin
from passlib.context import CryptContext
from jose import jwt
import os

router = APIRouter(prefix="/admin", tags=["Admin"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_secret_key")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(admin_id: int):
    payload = {"admin_id": admin_id}
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

# -------- Registration --------
@router.post("/register", response_model=Token)
def register_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    existing = db.query(Admin).filter(Admin.email == admin.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_admin = Admin(
        name=admin.name,
        email=admin.email,
        password_hash=hash_password(admin.password),
        role=admin.role
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    token = create_access_token(new_admin.admin_id)
    return {"access_token": token, "token_type": "bearer"}

# -------- Login --------
@router.post("/login", response_model=Token)
def login_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    db_admin = db.query(Admin).filter(Admin.email == admin.email).first()
    if not db_admin:
        raise HTTPException(status_code=401, detail="Email not registered")
    if not verify_password(admin.password, db_admin.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect password")
    token = create_access_token(db_admin.admin_id)
    return {"access_token": token, "token_type": "bearer"}

# -------- Get Current Admin --------
@router.get("/me", response_model=AdminOut)
def get_me(current_admin: Admin = Depends(get_current_admin)):
    return current_admin
