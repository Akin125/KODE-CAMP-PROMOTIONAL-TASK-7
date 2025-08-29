# Task 5: Contact Manager API

A complete Contact Management System using SQLModel + FastAPI + Security with JWT authentication, dependency injection, and IP logging.

## Features

- **Complete Contact Management**: Full CRUD operations for contacts
- **User-Specific Access**: Each user can only access their own contacts
- **JWT Authentication**: Secure token-based authentication
- **Dependency Injection**: Proper DB session management
- **IP Address Logging**: Middleware logs all client IP addresses
- **Search Functionality**: Search contacts by name or email
- **CORS Support**: Cross-origin resource sharing enabled
- **Foreign Key Relationships**: Proper relational database design

## Project Structure

```
task5_contact_manager/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app with IP logging middleware
│   ├── models.py            # Contact and User models with relationships
│   ├── database.py          # Database configuration with dependency injection
│   ├── auth.py              # JWT authentication system
│   └── routers/
│       ├── __init__.py
│       ├── contacts.py      # Contact CRUD operations
│       └── users.py         # User authentication
├── main.py                  # Application entry point (port 8004)
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

The API will be available at `http://localhost:8004`

## Default Credentials

- Username: `contactuser`
- Password: `contact123`

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login to get JWT token
- `GET /auth/me` - Get current user information

### Contact Management
- `POST /contacts/` - Add new contact (logged-in user only)
- `GET /contacts/` - List user's contacts
- `GET /contacts/{id}` - Get specific contact
- `PUT /contacts/{id}` - Update contact
- `DELETE /contacts/{id}` - Delete contact

### Search Functionality
- `GET /contacts/search/by-name?name=John` - Search contacts by name
- `GET /contacts/search/by-email?email=john` - Search contacts by email

## Usage Example

1. Register a new user:
```bash
curl -X POST "http://localhost:8004/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "newuser", "email": "newuser@example.com", "password": "password123"}'
```

2. Login to get JWT token:
```bash
curl -X POST "http://localhost:8004/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "contactuser", "password": "contact123"}'
```

3. Create a contact:
```bash
curl -X POST "http://localhost:8004/contacts/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com", "phone": "+1234567890"}'
```

4. List all contacts:
```bash
curl "http://localhost:8004/contacts/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

5. Update a contact:
```bash
curl -X PUT "http://localhost:8004/contacts/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Smith", "phone": "+1987654321"}'
```

6. Search contacts by name:
```bash
curl "http://localhost:8004/contacts/search/by-name?name=John" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Security Features

### JWT Authentication
- Secure token-based authentication
- 30-minute token expiration
- Bearer token authorization
- Password hashing with bcrypt

### User Isolation
- Foreign key relationship between users and contacts
- Users can only access their own contacts
- Automatic user_id assignment on contact creation

### IP Logging
- Every request logs client IP address
- Comprehensive request details saved to `ip_logs.json`
- Client IP included in response headers

## Database Schema

### Users Table
- id (Primary Key)
- username (Unique)
- email (Unique)
- hashed_password
- created_at

### Contacts Table
- id (Primary Key)
- name
- email
- phone
- user_id (Foreign Key → users.id)
- created_at
- updated_at

## Files Generated

- `contacts.db` - SQLite database with relational schema
- `ip_logs.json` - IP address and request logging
- JWT tokens for secure authentication

## Response Headers

All responses include:
- `X-Client-IP` - Client's IP address
- Standard CORS headers for cross-origin support
