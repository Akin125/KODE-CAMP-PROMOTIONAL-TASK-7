# KODE CAMP PROMOTIONAL TASK 7 - FastAPI Projects

This repository contains 5 complete FastAPI projects demonstrating various backend development concepts including authentication, database management, middleware, and API design.

## Project Overview

### Task 1: Student Management System (Port 8000)
**Features**: Student CRUD, Grade management, JSON-based authentication, Request logging
- **Database**: SQLite with SQLModel ORM
- **Security**: JSON file-based user storage
- **Middleware**: Request logging to file
- **CORS**: Configured for http://localhost:3000

### Task 2: E-Commerce API (Port 8001)
**Features**: Modular structure, Product management, Shopping cart, JWT authentication
- **Database**: SQLite with relational models
- **Security**: JWT tokens with role-based access (admin/user)
- **Middleware**: Response time measurement
- **Backup**: Orders saved to orders.json

### Task 3: Job Application Tracker (Port 8002)
**Features**: Job application tracking, Search functionality, User-specific access
- **Database**: SQLite with foreign key relationships
- **Security**: JWT authentication with user isolation
- **Middleware**: User-Agent header validation
- **Search**: Filter by status, company, position

### Task 4: Notes API (Port 8003)
**Features**: Note management, Request counting, Multi-origin CORS
- **Database**: SQLite with automatic JSON backup
- **Middleware**: Request counting and logging
- **Backup**: Auto-save to notes.json
- **CORS**: Multiple origins (localhost:3000, 127.0.0.1:5500)

### Task 5: Contact Manager API (Port 8004)
**Features**: Complete contact system, JWT auth, IP logging
- **Database**: SQLite with foreign key relationships
- **Security**: JWT authentication with dependency injection
- **Middleware**: IP address logging to JSON
- **Search**: Name and email search functionality

## Project Structure

```
KODE-CAMP-PROMOTIONAL-TASK-7/
├── libraryBox/                    # Virtual environment
├── task1_student_management/      # Port 8000
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── database.py
│   │   ├── auth.py
│   │   └── routers/
│   │       ├── auth.py
│   │       └── students.py
│   ├── main.py
│   ├── requirements.txt
│   └── README.md
├── task2_ecommerce_api/           # Port 8001
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── database.py
│   │   ├── auth.py
│   │   └── routers/
│   │       ├── products.py
│   │       ├── cart.py
│   │       └── users.py
│   ├── main.py
│   ├── requirements.txt
│   └── README.md
├── task3_job_tracker/             # Port 8002
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── database.py
│   │   ├── auth.py
│   │   └── routers/
│   │       ├── applications.py
│   │       └── users.py
│   ├── main.py
│   ├── requirements.txt
│   └── README.md
├── task4_notes_api/               # Port 8003
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── database.py
│   │   └── routers/
│   │       └── notes.py
│   ├── main.py
│   ├── requirements.txt
│   └── README.md
└── task5_contact_manager/         # Port 8004
    ├── app/
    │   ├── main.py
    │   ├── models.py
    │   ├── database.py
    │   ├── auth.py
    │   └── routers/
    │       ├── contacts.py
    │       └── users.py
    ├── main.py
    ├── requirements.txt
    └── README.md
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)

### Quick Start
1. Clone the repository
2. Navigate to any task folder
3. Install dependencies: `pip install -r requirements.txt`
4. Run the application: `python main.py`

### Running All Applications
Each task runs on a different port, so you can run them simultaneously:

```bash
# Terminal 1 - Student Management
cd task1_student_management && python main.py  # Port 8000

# Terminal 2 - E-Commerce API
cd task2_ecommerce_api && python main.py       # Port 8001

# Terminal 3 - Job Tracker
cd task3_job_tracker && python main.py         # Port 8002

# Terminal 4 - Notes API
cd task4_notes_api && python main.py           # Port 8003

# Terminal 5 - Contact Manager
cd task5_contact_manager && python main.py     # Port 8004
```

## Default Credentials

| Task | Username | Password | Role/Notes |
|------|----------|----------|------------|
| Task 1 | admin | admin123 | JSON-based auth |
| Task 2 | admin / user | admin123 / user123 | Admin & User roles |
| Task 3 | jobseeker | password123 | Regular user |
| Task 4 | N/A | N/A | No authentication |
| Task 5 | contactuser | contact123 | JWT auth |

## Technologies Used

- **FastAPI**: Modern Python web framework
- **SQLModel**: SQL databases with Python type hints
- **JWT**: JSON Web Tokens for authentication
- **BCrypt**: Password hashing
- **SQLite**: Lightweight database for all projects
- **Uvicorn**: ASGI server for running applications
- **Pydantic**: Data validation and serialization

## Key Features Demonstrated

### Authentication & Security
- JSON file-based authentication (Task 1)
- JWT tokens with role-based access (Tasks 2, 3, 5)
- Password hashing with BCrypt
- Protected endpoints with dependency injection

### Database Management
- SQLModel ORM for type-safe database operations
- Foreign key relationships
- Automatic table creation
- Session management with dependency injection

### Middleware Implementation
- Request logging (Task 1)
- Response time measurement (Task 2)
- User-Agent validation (Task 3)
- Request counting (Task 4)
- IP address logging (Task 5)

### API Design Patterns
- RESTful endpoint design
- Proper HTTP status codes
- Request/Response models
- Error handling
- Search and filtering

### Cross-Origin Support
- CORS middleware configuration
- Multiple origin support
- Credential handling

## API Documentation

Each application provides interactive API documentation at:
- Swagger UI: `http://localhost:PORT/docs`
- ReDoc: `http://localhost:PORT/redoc`

## Files Generated During Runtime

### Task 1
- `student_management.db` - Student and grade data
- `users.json` - User credentials
- `requests.log` - Request logging

### Task 2
- `ecommerce.db` - Products, users, cart, orders
- `orders.json` - Order backup

### Task 3
- `job_tracker.db` - Job applications and users

### Task 4
- `notes.db` - Notes data
- `notes.json` - Notes backup
- `request_logs.json` - Request statistics

### Task 5
- `contacts.db` - Contacts and users
- `ip_logs.json` - IP address logs

## Development Notes

- All applications use SQLite for simplicity
- Each task is completely independent
- Proper error handling and validation
- Clean project structure with separation of concerns
- Comprehensive logging and monitoring

## Git Commits

The project follows proper git practices with at least 3 commits per task:
1. Initial setup
2. Add features
3. Add security/middleware

Total commits: 15+ commits documenting the development process
