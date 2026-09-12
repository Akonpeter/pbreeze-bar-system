from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import Base, engine, get_db

from app.models import Category, Product, Inventory, User
from app.routers.auth import router as auth_router



  #Create database tables
Base.metadata.create_all(bind=engine)


  # Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="Sales, Inventory, Purchase and Business Management API",
    version=settings.app_version,
)

  # Add Authentication routes
app.include_router(auth_router)

@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.app_name}",
        "status": "running",
        "version": settings.app_version,
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/database-test")
def database_test(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))

    return {
        "database": "connected successfully"
    }










    