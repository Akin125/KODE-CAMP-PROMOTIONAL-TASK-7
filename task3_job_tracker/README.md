# Task 3: Job Application Tracker

A FastAPI system for tracking job applications with user-specific access control and search functionality.

## Features

- **Job Application Management**: Track applications with company, position, status, and dates
- **User-Specific Access**: Users can only see and manage their own applications
- **Search Functionality**: Filter applications by status, company, or position
- **Authentication Required**: All application operations require login
- **User-Agent Validation**: Middleware rejects requests without User-Agent header
- **Error Handling**: Comprehensive error handling for invalid queries
- **SQLModel Database**: Relational database with proper foreign keys

## Project Structure

```
task3_job_tracker/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app with User-Agent middleware
│   ├── models.py            # JobApplication and User models
│   ├── database.py          # Database configuration
│   ├── auth.py              # JWT authentication
│   └── routers/
│       ├── __init__.py
│       ├── applications.py  # Job application CRUD and search
│       └── users.py         # User authentication
├── main.py                  # Application entry point (port 8002)
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

The API will be available at `http://localhost:8002`

## Default Credentials

- Username: `jobseeker`
- Password: `password123`

## Application Status Options

- `pending` - Application is pending
- `applied` - Application has been submitted
- `interview` - Interview scheduled/completed
- `rejected` - Application rejected
- `accepted` - Application accepted

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login to get JWT token
- `GET /auth/me` - Get current user info

### Job Applications
- `POST /applications/` - Add new job application
- `GET /applications/` - List all user's applications
- `GET /applications/search?status=pending` - Search applications by status
- `GET /applications/search?company=Google` - Search by company
- `GET /applications/search?position=Developer` - Search by position
- `GET /applications/{id}` - Get specific application
- `PUT /applications/{id}` - Update application
- `DELETE /applications/{id}` - Delete application

## Usage Example

1. Register/Login:
```bash
curl -X POST "http://localhost:8002/auth/login" \
  -H "Content-Type: application/json" \
  -H "User-Agent: MyApp/1.0" \
  -d '{"username": "jobseeker", "password": "password123"}'
```

2. Create job application:
```bash
curl -X POST "http://localhost:8002/applications/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -H "User-Agent: MyApp/1.0" \
  -d '{"company": "Google", "position": "Software Engineer", "status": "applied"}'
```

3. Search applications:
```bash
curl "http://localhost:8002/applications/search?status=pending" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "User-Agent: MyApp/1.0"
```

## Important Notes

- All requests must include User-Agent header
- Users can only access their own job applications
- Search supports partial matching for company and position
- Invalid query parameters return 400 Bad Request
