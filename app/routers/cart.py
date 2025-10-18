# app/routers/cart.py
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.auth_utils import decode_access_token

router = APIRouter(prefix="/cart", tags=["Cart"])

# ---------------- Current user dependency ----------------
def get_current_user(authorization: str = Header(...), db: Session = Depends(database.get_db)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = authorization.replace("Bearer ", "")
    payload = decode_access_token(token)
    if not payload or "user_id" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(models.User).filter(models.User.user_id == int(payload["user_id"])).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# ---------------- View Cart ----------------
@router.get("/", response_model=schemas.CartOut)
def view_cart(current_user: models.User = Depends(get_current_user), db: Session = Depends(database.get_db)):
    cart = db.query(models.Cart).filter(models.Cart.user_id == current_user.user_id).first()
    if not cart:
        cart = models.Cart(user_id=current_user.user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return {"cart_id": cart.cart_id, "user_id": cart.user_id, "items": cart.items}

# ---------------- Add item to cart ----------------
@router.post("/items", response_model=schemas.CartItemOut)
def add_item(item: schemas.CartItemCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(database.get_db)):
    cart = db.query(models.Cart).filter(models.Cart.user_id == current_user.user_id).first()
    if not cart:
        cart = models.Cart(user_id=current_user.user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    product = db.get(models.Product, item.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.stock_qty < item.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    # Check if item already in cart
    cart_item = db.query(models.CartItem).filter(models.CartItem.cart_id == cart.cart_id,
                                                 models.CartItem.product_id == item.product_id).first()
    if cart_item:
        cart_item.quantity += item.quantity
        db.commit()
        db.refresh(cart_item)
        return cart_item

    cart_item = models.CartItem(cart_id=cart.cart_id, product_id=item.product_id, quantity=item.quantity)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item

# ---------------- Update cart item ----------------
@router.put("/items/{cart_item_id}", response_model=schemas.CartItemOut)
def update_item(cart_item_id: int, payload: schemas.CartItemCreate, current_user: models.User = Depends(get_current_user),
                db: Session = Depends(database.get_db)):
    cart_item = db.get(models.CartItem, cart_item_id)
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    if cart_item.cart.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not owner")
    
    cart_item.quantity = payload.quantity
    db.commit()
    db.refresh(cart_item)
    return cart_item

# ---------------- Delete cart item ----------------
@router.delete("/items/{cart_item_id}")
def delete_item(cart_item_id: int, current_user: models.User = Depends(get_current_user),
                db: Session = Depends(database.get_db)):
    cart_item = db.get(models.CartItem, cart_item_id)
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    if cart_item.cart.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not owner")

    db.delete(cart_item)
    db.commit()
    return {"detail": "Cart item deleted successfully"}
