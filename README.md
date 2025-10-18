# 🛒 E-Commerce Platform Backend
# 📌 Project Overview
• This project is a full-fledged E-Commerce backend built with FastAPI, SQLAlchemy, and PostgreSQL. It simulates a real-world online shopping platform where users can:
 - Browse products by categories
 - Add products to cart and place orders
 - Make payments and track shipping
 - Write reviews and manage wishlists
• Admins can manage products, categories, inventory, and monitor user activities. The project is designed with JWT-based authentication, secure endpoints, and a scalable relational database schema.

# 🎯 Objectives
The main goals of this project are:
1. Design a normalized ER diagram for an e-commerce system.
2. Build a RESTful API backend using FastAPI and SQLAlchemy.
3. Implement secure authentication for users and admins.
4. Track orders, payments, and shipping efficiently.
5. Ensure data consistency and audit logging.

# 🧩 How It Works
# 1. Users
 - Users can register, login, and manage their profile.
 - Add products to cart or wishlist.
 - Place orders and apply coupons for discounts.
 - Review products they purchased.
# 2. Admins
 - Create, update, and delete products and categories.
 - Manage inventory and stock.
 - View logs of user/admin actions for auditing.
# 3. Products & Categories
 - Products are linked to categories for easy browsing.
 - Each product has details like price, stock, description, and brand.
 - Inventory tracks product quantity and location.
# 4. Cart & Orders
 - Users can add multiple items to the cart.
 - When an order is placed:
 - Order items are created automatically
 - Payment and shipping entries are generated
 - One order → One payment and One shipping (1:1 relationship)
# 5. Payments & Shipping
 - Payment status is tracked (pending, completed, failed).
 - Shipping info includes courier, tracking number, and delivery status.
# 6. Reviews & Wishlist
 - Users can post reviews for products with rating and comments.
 - Wishlist allows users to save products for later purchase.
# 7. Coupons & Discounts
 - Admins can create coupons with percentage discounts and validity period.
 - Orders can apply coupons if they meet the minimum amount.
# 8. Audit Logs
 - Tracks all actions performed by users and admins.
 - Helps in monitoring changes and maintaining security.
   
# 🛠️ Tech Stack
• Backend Framework: FastAPI
• ORM & Database: SQLAlchemy & PostgreSQL
• Authentication: JWT (JSON Web Tokens)
• Password Security: bcrypt (via Passlib)
• Environment Management: python-dotenv
• Documentation: Swagger UI (auto-generated)
