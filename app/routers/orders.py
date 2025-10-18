# app/routers/orders.py
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from decimal import Decimal
from app import models, schemas, database
from app.auth_utils import decode_access_token

router = APIRouter(prefix="/orders", tags=["Orders"])

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

# ---------------- Checkout (Place Order) ----------------
@router.post("/checkout", response_model=schemas.OrderOut)
def checkout(order_in: schemas.OrderCreate, current_user: models.User = Depends(get_current_user),
             db: Session = Depends(database.get_db)):
    cart = db.query(models.Cart).filter(models.Cart.user_id == current_user.user_id).first()
    if not cart or not cart.items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total = Decimal(0)
    for ci in cart.items:
        product = db.get(models.Product, ci.product_id)
        if product.stock_qty < ci.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for {product.name}")
        total += product.price * ci.quantity

    # Create Order
    order = models.Order(
        user_id=current_user.user_id,
        total_amount=total,
        shipping_address=order_in.shipping_address or current_user.address
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    # Create Order Items & reduce stock
    for ci in cart.items:
        product = db.get(models.Product, ci.product_id)
        order_item = models.OrderItem(
            order_id=order.order_id,
            product_id=product.product_id,
            quantity=ci.quantity,
            unit_price=product.price,
            subtotal=product.price * ci.quantity
        )
        product.stock_qty -= ci.quantity
        db.add(order_item)

    # Clear Cart
    db.query(models.CartItem).filter(models.CartItem.cart_id == cart.cart_id).delete()

    # Initialize Payment & Shipping
    payment = models.Payment(
        order_id=order.order_id,
        payment_method="pending",
        amount=order.total_amount,
        status="pending"
    )
    shipping = models.Shipping(order_id=order.order_id, status="pending")
    db.add(payment)
    db.add(shipping)

    db.commit()
    db.refresh(order)
    return order

# ---------------- List Orders ----------------
@router.get("/", response_model=list[schemas.OrderOut])
def list_orders(current_user: models.User = Depends(get_current_user), db: Session = Depends(database.get_db)):
    return db.query(models.Order).filter(models.Order.user_id == current_user.user_id).all()

# ---------------- Get Single Order ----------------
@router.get("/{order_id}", response_model=schemas.OrderOut)
def get_order(order_id: int, current_user: models.User = Depends(get_current_user),
              db: Session = Depends(database.get_db)):
    order = db.get(models.Order, order_id)
    if not order or order.user_id != current_user.user_id:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
