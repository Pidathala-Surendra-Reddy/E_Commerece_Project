# app/routers/categories.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database

# Define the router
router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

# Create a new category
@router.post("/", response_model=schemas.CategoryOut)
def create_category(category: schemas.CategoryBase, db: Session = Depends(database.get_db)):
    new_category = models.Category(
        category_name=category.category_name,
        description=category.description
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

# Get list of all categories
@router.get("/", response_model=list[schemas.CategoryOut])
def list_categories(db: Session = Depends(database.get_db)):
    categories = db.query(models.Category).all()
    return categories

# Update a category
@router.put("/{category_id}", response_model=schemas.CategoryOut)
def update_category(category_id: int, category: schemas.CategoryBase, db: Session = Depends(database.get_db)):
    db_category = db.get(models.Category, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    db_category.category_name = category.category_name
    db_category.description = category.description
    db.commit()
    db.refresh(db_category)
    return db_category

# Delete a category
@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(database.get_db)):
    db_category = db.get(models.Category, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    db.delete(db_category)
    db.commit()
    return {"detail": "Category deleted successfully"}
