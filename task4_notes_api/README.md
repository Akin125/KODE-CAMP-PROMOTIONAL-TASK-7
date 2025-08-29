# Task 4: Notes API

A Notes management API with file & database storage, request counting middleware, and CORS support for multiple origins.

## Features

- **Note Management**: Create, read, update, delete notes
- **Dual Storage**: SQLite database + JSON backup file
- **Request Counting**: Middleware counts and logs all requests
- **Multiple CORS Origins**: Supports localhost:3000 and 127.0.0.1:5500
- **Request Statistics**: Track total requests and timing
- **Automatic Backup**: All notes saved to notes.json on changes

## Project Structure

```
task4_notes_api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app with request counting middleware
│   ├── models.py            # Note model definitions
│   ├── database.py          # Database configuration
│   └── routers/
│       ├── __init__.py
│       └── notes.py         # Note CRUD operations
├── main.py                  # Application entry point (port 8003)
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

The API will be available at `http://localhost:8003`

## API Endpoints

### Notes Management
- `POST /notes/` - Create a new note
- `GET /notes/` - List all notes
- `GET /notes/{id}` - Get specific note by ID
- `PUT /notes/{id}` - Update existing note
- `DELETE /notes/{id}` - Delete note

### Statistics
- `GET /` - Root endpoint with request count
- `GET /health` - Health check with statistics
- `GET /stats` - Detailed request statistics

## Usage Example

1. Create a note:
```bash
curl -X POST "http://localhost:8003/notes/" \
  -H "Content-Type: application/json" \
  -d '{"title": "Meeting Notes", "content": "Discussed project timeline and deliverables"}'
```

2. Get all notes:
```bash
curl "http://localhost:8003/notes/"
```

3. Update a note:
```bash
curl -X PUT "http://localhost:8003/notes/1" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Meeting Notes", "content": "Updated content with action items"}'
```

4. Delete a note:
```bash
curl -X DELETE "http://localhost:8003/notes/1"
```

## Features Details

### Request Counting Middleware
- Counts every HTTP request to the API
- Logs request details to `request_logs.json`
- Adds `X-Request-Count` header to responses
- Tracks method, URL, IP, user agent, and timestamp

### Automatic Backup
- Every note operation triggers backup to `notes.json`
- Backup includes all note data with timestamps
- Useful for data recovery and external processing

### CORS Configuration
- Supports multiple frontend origins
- Configured for `http://localhost:3000` (React dev server)
- Configured for `http://127.0.0.1:5500` (Live Server)

## Files Generated

- `notes.db` - SQLite database
- `notes.json` - Notes backup file
- `request_logs.json` - Request logging file

## Response Headers

All responses include:
- `X-Request-Count` - Total requests processed
- Standard CORS headers for cross-origin support
