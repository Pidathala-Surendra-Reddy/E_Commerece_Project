# app/main.py
from fastapi import FastAPI
from dotenv import load_dotenv
from app.database import engine, Base
from fastapi.openapi.utils import get_openapi

# Load environment variables
load_dotenv()

# Import routers
from app.routers import (
    users, categories, products, inventory, cart, orders,
    payments, shipping, reviews, coupons, wishlist, admin
)

# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app initialization
app = FastAPI(
    title="E-Commerce API",
    version="0.1.0",
    description="JWT-based authentication for Users and Admins with secure endpoints."
)

# Register routers
routers = [
    users, categories, products, inventory, cart, orders,
    payments, shipping, reviews, coupons, wishlist, admin
]

for r in routers:
    app.include_router(r.router)


# ✅ Add Bearer Auth to Swagger UI (so "Authorize" button appears)
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter: **Bearer &lt;your_token&gt;**"
        }
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
