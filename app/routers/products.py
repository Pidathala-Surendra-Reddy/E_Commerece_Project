# app/routers/products.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import models, schemas, database

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=schemas.ProductOut)
def create_product(p: schemas.ProductCreate, db: Session = Depends(database.get_db)):
    prod = models.Product(**p.dict())
    db.add(prod); db.commit(); db.refresh(prod)
    # create inventory record too
    inv = models.Inventory(product_id=prod.product_id, quantity=prod.stock_qty)
    db.add(inv); db.commit()
    return prod

@router.get("/", response_model=list[schemas.ProductOut])
def list_products(skip:int=0, limit:int=50, q: str | None = Query(None), db: Session = Depends(database.get_db)):
    qry = db.query(models.Product)
    if q: qry = qry.filter(models.Product.name.ilike(f"%{q}%"))
    return qry.offset(skip).limit(limit).all()

@router.get("/{product_id}", response_model=schemas.ProductOut)
def get_product(product_id: int, db: Session = Depends(database.get_db)):
    p = db.get(models.Product, product_id)
    if not p: raise HTTPException(404, "Product not found")
    return p

@router.put("/{product_id}", response_model=schemas.ProductOut)
def update_product(product_id: int, data: schemas.ProductCreate, db: Session = Depends(database.get_db)):
    p = db.get(models.Product, product_id)
    if not p: raise HTTPException(404, "Product not found")
    for k,v in data.dict().items(): setattr(p, k, v)
    db.commit(); db.refresh(p)
    # update inventory if stock_qty changed
    if p.inventory:
        p.inventory.quantity = p.stock_qty
        db.commit()
    return p

@router.delete("/{product_id}")
def delete_product(product_id:int, db: Session = Depends(database.get_db)):
    p = db.get(models.Product, product_id)
    if not p: raise HTTPException(404, "Product not found")
    db.delete(p); db.commit()
    return {"detail":"deleted"}
