from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
import time
from .database import engine, create_db_and_tables, get_session
from .routers import products, cart, users
from .auth import create_default_users

app = FastAPI(
    title="E-Commerce API",
    description="A modular FastAPI e-commerce system with cart and checkout",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_response_time_header(request: Request, call_next):
    """Middleware to measure response time and add it to headers"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Response-Time"] = f"{process_time:.4f}"
    return response


@app.on_event("startup")
def on_startup():
    """Initialize database and create default users"""
    create_db_and_tables()
    # Create default users
    session = Session(engine)
    create_default_users(session)
    session.close()


# Include routers
app.include_router(users.router)
app.include_router(products.router)
app.include_router(cart.router)


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Welcome to E-Commerce API",
        "docs": "/docs",
        "endpoints": {
            "products": "/products/",
            "cart": "/cart/",
            "users": "/users/",
            "admin": "/products/admin/"
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "e-commerce-api"}
