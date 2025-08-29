from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from .database import engine, create_db_and_tables, get_session
from .routers import applications, users
from .auth import create_default_user

app = FastAPI(
    title="Job Application Tracker",
    description="A FastAPI system for tracking job applications with user-specific access",
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
async def check_user_agent(request: Request, call_next):
    """Middleware to reject requests if User-Agent header is missing"""
    user_agent = request.headers.get("user-agent")
    if not user_agent:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User-Agent header is required"
        )

    response = await call_next(request)
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
app.include_router(applications.router)


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Job Application Tracker API",
        "docs": "/docs",
        "features": [
            "Track job applications",
            "Search by status, company, position",
            "User-specific access control",
            "User-Agent validation"
        ]
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "job-tracker-api"}
