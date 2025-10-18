# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.auth_utils import hash_password, verify_password, create_access_token, decode_access_token





router = APIRouter(prefix="/auth", tags=["Authentication"])

# ---------------- Helpers ----------------
def get_current_user(authorization: str = Header(...), db: Session = Depends(database.get_db)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Invalid authorization header")
    token = authorization.replace("Bearer ", "")
    payload = decode_access_token(token)
    if not payload or "user_id" not in payload:
        raise HTTPException(401, "Invalid token")
    user = db.query(models.User).filter(models.User.user_id == int(payload["user_id"])).first()
    if not user:
        raise HTTPException(401, "User not found")
    return user

def get_current_admin(authorization: str = Header(...), db: Session = Depends(database.get_db)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Invalid authorization header")
    token = authorization.replace("Bearer ", "")
    payload = decode_access_token(token)
    if not payload or "admin_id" not in payload:
        raise HTTPException(401, "Invalid token")
    admin = db.query(models.Admin).filter(models.Admin.admin_id == int(payload["admin_id"])).first()
    if not admin:
        raise HTTPException(401, "Admin not found")
    return admin

# ---------------- User Registration/Login ----------------
@router.post("/user/register", response_model=schemas.UserOut)
def register_user(payload: schemas.UserCreate, db: Session = Depends(database.get_db)):
    if db.query(models.User).filter(models.User.email == payload.email).first():
        raise HTTPException(400, "Email already registered")
    user = models.User(
        name=payload.name,
        email=payload.email,
        password=hash_password(payload.password),
        phone=payload.phone,
        address=payload.address
    )
    db.add(user); db.commit(); db.refresh(user)
    return user

@router.post("/user/login", response_model=schemas.Token)
def login_user(payload: schemas.UserCreate, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(401, "Invalid credentials")
    token = create_access_token({"user_id": user.user_id})
    return {"access_token": token, "token_type": "bearer"}

# ---------------- Admin Registration/Login ----------------
@router.post("/admin/register", response_model=schemas.AdminOut)
def register_admin(payload: schemas.AdminCreate, db: Session = Depends(database.get_db)):
    if db.query(models.Admin).filter(models.Admin.email == payload.email).first():
        raise HTTPException(400, "Admin email already registered")
    admin = models.Admin(
        name=payload.name,
        email=payload.email,
        password=hash_password(payload.password)
    )
    db.add(admin); db.commit(); db.refresh(admin)
    return admin

@router.post("/admin/login", response_model=schemas.Token)
def login_admin(payload: schemas.AdminCreate, db: Session = Depends(database.get_db)):
    admin = db.query(models.Admin).filter(models.Admin.email == payload.email).first()
    if not admin or not verify_password(payload.password, admin.password):
        raise HTTPException(401, "Invalid credentials")
    token = create_access_token({"admin_id": admin.admin_id})
    return {"access_token": token, "token_type": "bearer"}
