from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.auth_utils import decode_access_token

router = APIRouter(prefix="/wishlist", tags=["Wishlist"])

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

@router.post("/", response_model=schemas.WishlistOut)
def add_wishlist(payload: dict, user: models.User = Depends(get_current_user), db: Session = Depends(database.get_db)):
    product = db.get(models.Product, int(payload["product_id"]))
    if not product: raise HTTPException(404, "Product not found")
    w = models.Wishlist(user_id=user.user_id, product_id=product.product_id)
    db.add(w); db.commit(); db.refresh(w)
    return w

@router.get("/{user_id}", response_model=list[schemas.WishlistOut])
def get_wishlist(user_id:int, db: Session = Depends(database.get_db)):
    return db.query(models.Wishlist).filter(models.Wishlist.user_id == user_id).all()
