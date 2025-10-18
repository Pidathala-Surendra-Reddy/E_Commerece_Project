# app/routers/payments.py
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from datetime import datetime
from app import models, schemas, database
from app.auth_utils import decode_access_token

router = APIRouter(prefix="/payments", tags=["Payments"])


# Dependency to get the current logged-in user
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


# Complete a payment for a given order
@router.post("/{order_id}/complete")
def complete_payment(
    order_id: int,
    transaction: schemas.PaymentTransaction,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Marks a payment as completed for a specific order.
    """
    # Get the order
    order = db.get(models.Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Ensure the order belongs to the current user
    if order.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not allowed to complete payment for this order")
    
    # Get the payment record
    payment = db.query(models.Payment).filter(models.Payment.order_id == order_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment record not found")
    
    # Update payment
    payment.status = "paid"
    payment.transaction_id = transaction.transaction_id
    payment.created_at = datetime.utcnow()
    
    # Update order status
    order.status = "processing"
    
    db.commit()
    db.refresh(payment)
    db.refresh(order)
    
    return {
        "detail": "Payment marked as paid",
        "order_id": order.order_id,
        "payment_id": payment.payment_id,
        "status": payment.status
    }
