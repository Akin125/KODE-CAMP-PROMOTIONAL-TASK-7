# Task 2: E-Commerce API

A modular FastAPI e-commerce system with cart functionality, checkout system, and JWT authentication.

## Features

- **Modular Structure**: Separate routers for products, cart, and users
- **Product Management**: Admin-only product creation, public product viewing
- **Shopping Cart**: Add items, view cart, remove items
- **Checkout System**: Complete orders with stock validation
- **JWT Authentication**: Secure user authentication with role-based access
- **Response Time Middleware**: Measures and adds response time to headers
- **Order Backup**: Saves orders to orders.json file
- **CORS Support**: Cross-origin resource sharing enabled

## Project Structure

```
task2_ecommerce_api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app with middleware
│   ├── models.py            # SQLModel definitions
│   ├── database.py          # Database configuration
│   ├── auth.py              # JWT authentication
│   └── routers/
│       ├── __init__.py
│       ├── products.py      # Product management
│       ├── cart.py          # Shopping cart functionality
│       └── users.py         # User management
├── main.py                  # Application entry point
├── requirements.txt         # Dependencies
└── README.md               # This file
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

The API will be available at `http://localhost:8001`

## Default Credentials

### Admin User
- Username: `admin`
- Password: `admin123`
- Role: `admin`

### Regular User
- Username: `user`
- Password: `user123`
- Role: `user`

## API Endpoints

### Authentication
- `POST /users/register` - Register new user
- `POST /users/login` - Login to get JWT token
- `GET /users/me` - Get current user info

### Products (Public)
- `GET /products/` - List all products
- `GET /products/{id}` - Get specific product

### Products (Admin Only)
- `POST /products/admin/` - Create new product
- `PUT /products/admin/{id}` - Update product
- `DELETE /products/admin/{id}` - Delete product

### Shopping Cart
- `POST /cart/add` - Add item to cart
- `GET /cart/` - View cart items
- `DELETE /cart/remove/{item_id}` - Remove item from cart
- `POST /cart/checkout` - Checkout and create order

## Usage Example

1. Login as admin:
```bash
curl -X POST "http://localhost:8001/users/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

2. Create a product (admin):
```bash
curl -X POST "http://localhost:8001/products/admin/" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "price": 999.99, "stock": 10, "description": "High-end laptop"}'
```

3. Add to cart (user):
```bash
curl -X POST "http://localhost:8001/cart/add" \
  -H "Authorization: Bearer YOUR_USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 2}'
```

4. Checkout:
```bash
curl -X POST "http://localhost:8001/cart/checkout" \
  -H "Authorization: Bearer YOUR_USER_TOKEN"
```

## Files Generated

- `ecommerce.db` - SQLite database
- `orders.json` - Order backup file
- Response time headers in all API responses
