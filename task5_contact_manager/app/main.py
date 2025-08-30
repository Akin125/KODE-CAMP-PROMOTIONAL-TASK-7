from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
import json
import os
from datetime import datetime
from .database import engine, create_db_and_tables, get_session
from .routers import contacts, users
from .auth import create_default_user

app = FastAPI(
    title="Contact Manager API",
    description="A complete Contact Management System using SQLModel + FastAPI + Security",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_ip_address(request: Request, call_next):
    """Middleware to log IP address of every request"""
    client_ip = request.client.host
    user_agent = request.headers.get("user-agent", "Unknown")
    method = request.method
    url = str(request.url)
    timestamp = datetime.utcnow().isoformat()

    # Log to file
    log_entry = {
        "timestamp": timestamp,
        "ip_address": client_ip,
        "method": method,
        "url": url,
        "user_agent": user_agent
    }

    # Save to IP log file
    ip_log_file = "ip_logs.json"
    if os.path.exists(ip_log_file):
        with open(ip_log_file, "r") as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append(log_entry)

    with open(ip_log_file, "w") as f:
        json.dump(logs, f, indent=2)

    response = await call_next(request)
    response.headers["X-Client-IP"] = client_ip
    return response


@app.on_event("startup")
def on_startup():
    """Initialize database and create default user"""
    create_db_and_tables()
    # Create default user
    session = Session(engine)
    create_default_user(session)
    session.close()


# Include routers
app.include_router(users.router)
app.include_router(contacts.router)


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Contact Manager API",
        "docs": "/docs",
        "features": [
            "Complete contact management system",
            "JWT-based authentication",
            "User-specific contact access",
            "IP address logging",
            "CORS enabled",
            "Dependency injection for DB"
        ]
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "contact-manager-api",
        "timestamp": datetime.utcnow()
    }


@app.get("/logs")
def get_logs():
    """get logs endpoint"""
    ip_log_file = "ip_logs.json"
    if os.path.exists(ip_log_file):
        with open(ip_log_file, "r") as f:
            logs = json.load(f)
            return {"logs": logs}
    else:
        return {"logs": [], "message": "No logs found"}