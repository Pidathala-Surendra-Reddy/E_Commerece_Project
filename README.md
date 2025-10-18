# 🛒 E-Commerce Platform
 # 📌 Overview
• This project is a complete E-Commerce Platform backend built with FastAPI, SQLAlchemy, and PostgreSQL. It supports:
• User registration, authentication, and profile management
• Product management and browsing
• Shopping cart, orders, and payments
• Reviews, wishlists, and coupons
• Admin and inventory management
• JWT-based authentication for secure endpoints
• The backend is designed to be scalable, secure, and ready for production, with a normalized relational database schema.

# 🎯 Objective
• The goal of this project is to:
• Design a fully-functional ER diagram for an e-commerce system.
• Implement a FastAPI backend using SQLAlchemy ORM.
• Demonstrate JWT-based authentication for users and admins.
• Provide RESTful APIs for all major e-commerce operations.
• Ensure data integrity, relationships, and cascading actions.


# 🏗️ Project Structure
e-commerce/
│
├─ app/
│  ├─ main.py              # FastAPI app initialization
│  ├─ models.py            # SQLAlchemy ORM models
│  ├─ database.py          # Database setup (PostgreSQL)
│  ├─ auth_utils.py        # Password hashing and JWT token utils
│  ├─ dependencies.py      # Current user/admin dependency functions
│  ├─ schemas.py           # Pydantic schemas for request/response validation
│  └─ routers/
│      ├─ users.py
│      ├─ admin.py
│      ├─ products.py
│      ├─ categories.py
│      ├─ inventory.py
│      ├─ cart.py
│      ├─ orders.py
│      ├─ payments.py
│      ├─ shipping.py
│      ├─ reviews.py
│      ├─ coupons.py
│      └─ wishlist.py
│
├─ .env                    # Environment variables (DB URL, JWT secret)
├─ requirements.txt        # Python dependencies
└─ README.md

# ⚡ Key Features
1. Authentication & Authorization:
  • JWT-based login for Users and Admins
  • Protected routes with get_current_user and get_current_admin dependencies
2. Product & Category Management:
   • Admins can create, update, delete categories and products
   • Products linked to categories for filtering
3. Shopping Cart & Orders:
   • Users can add products to cart
   • Place orders and generate order items automatically
   • Apply coupons and calculate total amounts
4. Payment & Shipping:
   • One-to-one relationship with each order
   • Track shipping status and estimated delivery
5. Reviews & Wishlist:
   • Users can review products
   • Add products to wishlist for later purchase
6. Inventory & Audit Logs
   • Track product stock and location
   • Log all actions performed by users and admins
   
# 🛠️ Tech Stack

• Backend Framework: FastAPI
• ORM & Database: SQLAlchemy & PostgreSQL
• Authentication: JWT (JSON Web Tokens)
• Password Security: bcrypt (via Passlib)
• Environment Management: python-dotenv
• Documentation: Swagger UI (auto-generated)

# ⚙️ Setup Instructions

# 1. Clone the repository:
 - git clone https://github.com/Pidathala-Surendra-Reddy/E_Commerece_Project.git
 - cd E_Commerece_Project
# 2. Create a virtual environment:
 - python -m venv venv
 - source venv/bin/activate  # Linux/Mac
 - venv\Scripts\activate     # Windows
# 3. Install dependencies:
 - pip install -r requirements.txt
# 4. Configure .env with:
 - DATABASE_URL=postgresql://username:password@localhost/dbname
 - JWT_SECRET_KEY=your_secret_key
 - JWT_ALGORITHM=HS256
# 5. Run the FastAPI server:
 - uvicorn app.main:app --reload
# 6. Access Swagger docs at:
http://127.0.0.1:8000/docs

📈 ER Diagram
A visual ER diagram representing all tables, relationships, PKs, and FKs should be included in /docs/ER_Diagram.png or exported from tools like dbdiagram.io, draw.io, or Lucidchart.
