# app/models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, DECIMAL, Boolean
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

# Utility function for timestamps
def now():
    return datetime.utcnow()

# -------------------- Admin --------------------
class Admin(Base):
    __tablename__ = "admins"
    admin_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    email = Column(String(200), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), default="manager")
    created_at = Column(DateTime, default=now)

    # Relationships
    products = relationship("Product", back_populates="admin")
    categories = relationship("Category", back_populates="admin")

# -------------------- User --------------------
class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    email = Column(String(200), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    phone = Column(String(30), nullable=True)
    address = Column(Text, nullable=True)
    created_at = Column(DateTime, default=now)

    # Relationships
    cart = relationship("Cart", back_populates="user", uselist=False, cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="user")
    reviews = relationship("Review", back_populates="user")
    wishlist = relationship("Wishlist", back_populates="user")

# -------------------- Category --------------------
class Category(Base):
    __tablename__ = "categories"
    category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    admin_id = Column(Integer, ForeignKey("admins.admin_id"), nullable=True)

    # Relationships
    admin = relationship("Admin", back_populates="categories")
    products = relationship("Product", back_populates="category")

# -------------------- Product --------------------
class Product(Base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    brand = Column(String(100), nullable=True)
    price = Column(DECIMAL(12, 2), nullable=False)
    stock_qty = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey("categories.category_id"), nullable=True)
    admin_id = Column(Integer, ForeignKey("admins.admin_id"), nullable=True)
    created_at = Column(DateTime, default=now)
    is_active = Column(Boolean, default=True)

    # Relationships
    category = relationship("Category", back_populates="products")
    admin = relationship("Admin", back_populates="products")
    inventory = relationship("Inventory", back_populates="product", uselist=False, cascade="all, delete-orphan")
    order_items = relationship("OrderItem", back_populates="product")
    cart_items = relationship("CartItem", back_populates="product")
    reviews = relationship("Review", back_populates="product")
    wishlists = relationship("Wishlist", back_populates="product")

# -------------------- Inventory --------------------
class Inventory(Base):
    __tablename__ = "inventory"
    inventory_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), unique=True)
    quantity = Column(Integer, default=0)
    location = Column(String(200), nullable=True)
    last_updated = Column(DateTime, default=now)

    product = relationship("Product", back_populates="inventory")

# -------------------- Cart --------------------
class Cart(Base):
    __tablename__ = "carts"
    cart_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), unique=True)
    created_at = Column(DateTime, default=now)

    user = relationship("User", back_populates="cart")
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")

class CartItem(Base):
    __tablename__ = "cart_items"
    cart_item_id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.cart_id"))
    product_id = Column(Integer, ForeignKey("products.product_id"))
    quantity = Column(Integer, nullable=False, default=1)

    cart = relationship("Cart", back_populates="items")
    product = relationship("Product", back_populates="cart_items")

# -------------------- Order --------------------
class Order(Base):
    __tablename__ = "orders"
    order_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    order_date = Column(DateTime, default=now)
    status = Column(String(50), default="pending")
    total_amount = Column(DECIMAL(12, 2), nullable=False, default=0)
    shipping_address = Column(Text, nullable=True)
    coupon_id = Column(Integer, ForeignKey("coupons.coupon_id"), nullable=True)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    payment = relationship("Payment", back_populates="order", uselist=False, cascade="all, delete-orphan")
    shipping = relationship("Shipping", back_populates="order", uselist=False, cascade="all, delete-orphan")
    coupon = relationship("Coupon", back_populates="orders")

class OrderItem(Base):
    __tablename__ = "order_items"
    order_item_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"))
    product_id = Column(Integer, ForeignKey("products.product_id"))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL(12, 2), nullable=False)
    subtotal = Column(DECIMAL(12, 2), nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

# -------------------- Payment --------------------
class Payment(Base):
    __tablename__ = "payments"
    payment_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), unique=True)
    payment_method = Column(String(50), nullable=False)
    amount = Column(DECIMAL(12, 2), nullable=False)
    status = Column(String(50), default="pending")
    transaction_id = Column(String(200), nullable=True)
    created_at = Column(DateTime, default=now)

    order = relationship("Order", back_populates="payment")

# -------------------- Shipping --------------------
class Shipping(Base):
    __tablename__ = "shipping"
    shipment_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), unique=True)
    courier_name = Column(String(200), nullable=True)
    tracking_number = Column(String(200), nullable=True)
    status = Column(String(50), default="pending")
    estimated_delivery = Column(DateTime, nullable=True)
    delivered_at = Column(DateTime, nullable=True)

    order = relationship("Order", back_populates="shipping")

# -------------------- Review --------------------
class Review(Base):
    __tablename__ = "reviews"
    review_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    product_id = Column(Integer, ForeignKey("products.product_id"))
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=now)

    user = relationship("User", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")

# -------------------- Coupon --------------------
class Coupon(Base):
    __tablename__ = "coupons"
    coupon_id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    discount_percent = Column(Integer, nullable=True)
    active = Column(Boolean, default=True)
    valid_from = Column(DateTime, nullable=True)
    valid_until = Column(DateTime, nullable=True)
    min_amount = Column(DECIMAL(12, 2), nullable=True)

    orders = relationship("Order", back_populates="coupon")

# -------------------- Wishlist --------------------
class Wishlist(Base):
    __tablename__ = "wishlists"
    wishlist_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    product_id = Column(Integer, ForeignKey("products.product_id"))
    added_at = Column(DateTime, default=now)

    user = relationship("User", back_populates="wishlist")
    product = relationship("Product", back_populates="wishlists")

# -------------------- Audit Log --------------------
class AuditLog(Base):
    __tablename__ = "audit_logs"
    audit_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    admin_id = Column(Integer, ForeignKey("admins.admin_id"), nullable=True)
    action = Column(String(255), nullable=False)
    entity = Column(String(100), nullable=True)
    entity_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=now)
