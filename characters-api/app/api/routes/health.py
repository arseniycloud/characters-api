"""Health check and database connection routes."""
from typing import Dict
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db_session
from app.services.character_service import CharacterService

router = APIRouter()


@router.get("/")
async def read_root():
    """Welcome message for the root route."""
    return {"message": "Welcome to my FastAPI application!"}


@router.get("/test-db")
async def test_db(db: Session = Depends(get_db_session)):
    """Test database connection."""
    is_connected = CharacterService.check_db_connection(db)

    if is_connected:
        return {"status": "Database connection successful"}
    else:
        return {"status": "Database error"}
