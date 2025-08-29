)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware to log every request"""
    start_time = time.time()

    # Log request details
    client_ip = request.client.host
    method = request.method
    url = str(request.url)

    response = await call_next(request)

    process_time = time.time() - start_time

    # Log the request
    log_message = f"IP: {client_ip} | Method: {method} | URL: {url} | Status: {response.status_code} | Time: {process_time:.4f}s"
    logger.info(log_message)

    return response


@app.on_event("startup")
def on_startup():
    """Initialize database and create default user"""
    create_db_and_tables()
    create_default_user()


# Include routers
app.include_router(auth.router)
app.include_router(students.router)


@app.get("/")
def root():
    """Root endpoint"""
    return {"message": "Welcome to Student Management System API"}


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow()}
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
import time
import logging
from datetime import datetime
from .database import engine, create_db_and_tables
from .routers import students, auth
from .auth import create_default_user

# Configure logging
logging.basicConfig(
    filename="requests.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Student Management System",
    description="A FastAPI backend for managing students and their grades",
    version="1.0.0"
