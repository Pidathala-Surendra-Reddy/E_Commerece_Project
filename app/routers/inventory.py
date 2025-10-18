# app/routers/inventory.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.get("/", response_model=list[schemas.InventoryOut])
def list_inventory(db: Session = Depends(database.get_db)):
    return db.query(models.Inventory).all()

@router.put("/{product_id}", response_model=schemas.InventoryOut)
def update_inventory(product_id: int, payload: dict, db: Session = Depends(database.get_db)):
    inv = db.query(models.Inventory).filter(models.Inventory.product_id == product_id).first()
    if not inv:
        raise HTTPException(404, "Inventory record not found")
    inv.quantity = int(payload.get("quantity", inv.quantity))
    db.commit(); db.refresh(inv)
    return inv
