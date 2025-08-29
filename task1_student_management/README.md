- `PUT /students/{id}` - Update student (requires auth)
- `DELETE /students/{id}` - Delete student (requires auth)
- `POST /students/{id}/grades` - Add grade to student (requires auth)
- `GET /students/{id}/grades` - Get student's grades

## Usage Example

1. Login to get token:
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

2. Create a student (use token from step 1):
```bash
curl -X POST "http://localhost:8000/students/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "age": 20, "email": "john@example.com"}'
```

## Files Generated

- `student_management.db` - SQLite database
- `users.json` - User credentials storage
- `requests.log` - Request logging file
# Task 1: Student Management System

A FastAPI backend for managing students and their grades with authentication, database storage, and middleware.

## Features

- **Student Management**: Full CRUD operations for students
- **Grade Management**: Add and view grades for students
- **Authentication**: JWT-based authentication with users stored in JSON
- **Database**: SQLite database with SQLModel ORM
- **Middleware**: Request logging and CORS support
- **Security**: Protected endpoints for creating/updating data

## Project Structure

```
task1_student_management/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app with middleware
│   ├── models.py            # SQLModel definitions
│   ├── database.py          # Database configuration
│   ├── auth.py              # Authentication logic
│   └── routers/
│       ├── __init__.py
│       ├── auth.py          # Authentication endpoints
│       └── students.py      # Student CRUD endpoints
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

The API will be available at `http://localhost:8000`

## Default Credentials

- Username: `admin`
- Password: `admin123`

## API Endpoints

### Authentication
- `POST /auth/login` - Login to get access token

### Students
- `GET /students/` - List all students
- `POST /students/` - Create new student (requires auth)
- `GET /students/{id}` - Get specific student
