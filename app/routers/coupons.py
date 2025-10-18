# app/routers/coupons.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database

router = APIRouter(prefix="/coupons", tags=["Coupons"])

@router.post("/", response_model=schemas.CouponOut)
def create_coupon(payload: schemas.CouponCreate, db: Session = Depends(database.get_db)):
    c = models.Coupon(**payload.dict())
    db.add(c); db.commit(); db.refresh(c); return c

@router.get("/", response_model=list[schemas.CouponOut])
def list_coupons(db: Session = Depends(database.get_db)):
    return db.query(models.Coupon).all()
