from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from datetime import datetime
from .database import create_db_and_tables
from .routers import notes

# Global request counter
request_count = 0

app = FastAPI(
    title="Notes API",
    description="A Notes management API with file & database storage",
    version="1.0.0"
)

# Add CORS middleware for multiple origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def count_and_log_requests(request: Request, call_next):
    """Middleware to count total requests made and log them"""
    global request_count
    request_count += 1

    # Log request details
    log_data = {
        "request_number": request_count,
        "timestamp": datetime.utcnow().isoformat(),
        "method": request.method,
        "url": str(request.url),
        "client_ip": request.client.host,
        "user_agent": request.headers.get("user-agent", "Unknown")
    }

    # Save log to file
    log_file = "request_logs.json"
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append(log_data)

    with open(log_file, "w") as f:
        json.dump(logs, f, indent=2)

    response = await call_next(request)
    response.headers["X-Request-Count"] = str(request_count)
    return response


@app.on_event("startup")
def on_startup():
    """Initialize database"""
    create_db_and_tables()


# Include routers
app.include_router(notes.router)


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Notes API",
        "docs": "/docs",
        "total_requests": request_count,
        "features": [
            "Create, read, update, delete notes",
            "Automatic JSON backup",
            "Request counting and logging",
            "CORS support for multiple origins"
        ]
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "notes-api",
        "total_requests": request_count,
        "timestamp": datetime.utcnow()
    }


@app.get("/stats")
def get_request_stats():
    """Get request statistics"""
    return {
        "total_requests": request_count,
        "timestamp": datetime.utcnow(),
        "log_file": "request_logs.json",
        "backup_file": "notes.json"
    }
