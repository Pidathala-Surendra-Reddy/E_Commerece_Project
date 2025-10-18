# app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# ---------------- User ----------------
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: Optional[str] = None
    address: Optional[str] = None

class UserOut(BaseModel):
    user_id: int
    name: str
    email: EmailStr
    phone: Optional[str]
    address: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}

# ---------------- Admin ----------------
class AdminCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Optional[str] = None

class AdminOut(BaseModel):
    admin_id: int
    name: str
    email: EmailStr
    role: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}

# ---------------- Category ----------------
class CategoryBase(BaseModel):
    category_name: str
    description: Optional[str] = None

class CategoryOut(CategoryBase):
    category_id: int
    model_config = {"from_attributes": True}

# ---------------- Product ----------------
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    brand: Optional[str] = None
    price: Decimal
    stock_qty: int
    category_id: Optional[int] = None

class ProductOut(ProductCreate):
    product_id: int
    model_config = {"from_attributes": True}

# ---------------- Cart ----------------
class CartItemCreate(BaseModel):
    product_id: int
    quantity: int

class CartItemOut(CartItemCreate):
    cart_item_id: int
    model_config = {"from_attributes": True}

class CartOut(BaseModel):
    cart_id: int
    user_id: int
    items: List[CartItemOut]
    model_config = {"from_attributes": True}

# ---------------- Order ----------------
class OrderCreate(BaseModel):
    shipping_address: Optional[str] = None

class OrderItemOut(BaseModel):
    order_item_id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    subtotal: Decimal
    model_config = {"from_attributes": True}

class OrderOut(BaseModel):
    order_id: int
    user_id: int
    total_amount: Decimal
    shipping_address: Optional[str] = None
    items: List[OrderItemOut] = []
    model_config = {"from_attributes": True}

# ---------------- Payment ----------------
class PaymentOut(BaseModel):
    payment_id: int
    order_id: int
    payment_method: str
    amount: Decimal
    status: str
    transaction_id: Optional[str] = None
    created_at: datetime
    model_config = {"from_attributes": True}

class PaymentTransaction(BaseModel):
    transaction_id: str

# ---------------- Shipping ----------------
class ShippingOut(BaseModel):
    shipment_id: int
    order_id: int
    courier_name: Optional[str] = None
    tracking_number: Optional[str] = None
    status: str
    estimated_delivery: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    model_config = {"from_attributes": True}

class ShippingUpdate(BaseModel):
    courier_name: Optional[str] = None
    tracking_number: Optional[str] = None
    status: Optional[str] = None
    estimated_delivery: Optional[datetime] = None

# ---------------- Review ----------------
class ReviewCreate(BaseModel):
    product_id: int
    rating: int
    comment: Optional[str] = None

class ReviewOut(ReviewCreate):
    review_id: int
    model_config = {"from_attributes": True}

# ---------------- Coupon ----------------
class CouponCreate(BaseModel):
    code: str
    description: Optional[str] = None
    discount_percent: Optional[int] = None
    active: Optional[bool] = True
    min_amount: Optional[Decimal] = None

class CouponOut(CouponCreate):
    coupon_id: int
    model_config = {"from_attributes": True}

# ---------------- Wishlist ----------------
class WishlistOut(BaseModel):
    wishlist_id: int
    user_id: int
    product_id: int
    added_at: datetime
    model_config = {"from_attributes": True}

# ---------------- Token ----------------
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ---------------- Inventory ----------------
class InventoryCreate(BaseModel):
    product_id: int
    stock_qty: int
    location: Optional[str] = None

class InventoryOut(BaseModel):
    inventory_id: int
    product_id: int
    stock_qty: int
    location: Optional[str] = None
    updated_at: datetime
    model_config = {"from_attributes": True}
# app/schemas.py

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

    model_config = {"from_attributes": True}
