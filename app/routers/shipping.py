# app/routers/shipping.py
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.auth_utils import decode_access_token

router = APIRouter(prefix="/shipping", tags=["Shipping"])

# Admin authentication
def get_current_admin(authorization: str = Header(...), db: Session = Depends(database.get_db)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = authorization.replace("Bearer ", "")
    payload = decode_access_token(token)
    if not payload or "admin_id" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    admin = db.query(models.Admin).filter(models.Admin.admin_id == int(payload["admin_id"])).first()
    if not admin:
        raise HTTPException(status_code=401, detail="Admin not found")
    return admin

# Update shipping info (admin only)
@router.put("/{order_id}/update", response_model=schemas.ShippingOut)
def update_shipping(order_id:int, payload: schemas.ShippingUpdate, 
                    admin: models.Admin = Depends(get_current_admin), 
                    db: Session = Depends(database.get_db)):
    ship = db.query(models.Shipping).filter(models.Shipping.order_id == order_id).first()
    if not ship: ship = models.Shipping(order_id=order_id)
    if payload.courier_name: ship.courier_name = payload.courier_name
    if payload.tracking_number: ship.tracking_number = payload.tracking_number
    if payload.status: ship.status = payload.status
    if payload.estimated_delivery: ship.estimated_delivery = payload.estimated_delivery
    db.add(ship)
    db.commit()
    db.refresh(ship)
    return ship

# Get shipping info
@router.get("/{order_id}", response_model=schemas.ShippingOut)
def get_shipping(order_id:int, db: Session = Depends(database.get_db)):
    ship = db.query(models.Shipping).filter(models.Shipping.order_id == order_id).first()
    if not ship:
        raise HTTPException(status_code=404, detail="Shipping info not found")
    return ship
