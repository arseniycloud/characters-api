"""Character API routes."""
from typing import Dict, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.dependencies import get_db_session
from app.services.character_service import CharacterService
from app.schemas import CharacterResponse, CharacterCreate

router = APIRouter()

# Constants
DATABASE_ERROR_MSG = "Database error"


@router.get("/", response_model=Dict[str, List[CharacterResponse]])
async def get_all_characters(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db_session)
):
    """Get a list of all characters with pagination."""
    characters = CharacterService.get_all_characters(db, skip=skip, limit=limit)
    return {"result": characters}


@router.get("/character", response_model=Dict[str, CharacterResponse])
async def get_character_by_name(
    name: str,
    db: Session = Depends(get_db_session)
):
    """Get a character by name."""
    character = CharacterService.get_character_by_name(name, db)
    return {"result": character}


@router.post("/character", status_code=200, response_model=Dict[str, CharacterResponse])
async def create_character(
    character_data: CharacterCreate,
    db: Session = Depends(get_db_session)
):
    """Create a new character."""
    try:
        new_character = CharacterService.create_character(character_data.dict(), db)
        return {"result": new_character}
    except HTTPException:
        raise
    except Exception as e:
        from app.config import setup_logging
        logger = setup_logging()
        logger.error(f"{DATABASE_ERROR_MSG} when creating character: {e}")
        raise HTTPException(status_code=500, detail=DATABASE_ERROR_MSG)


@router.put("/character", response_model=Dict[str, CharacterResponse])
async def update_character(
    character_data: CharacterCreate,
    db: Session = Depends(get_db_session)
):
    """Update an existing character."""
    try:
        character = CharacterService.update_character(character_data.dict(), db)
        return {"result": character}
    except HTTPException:
        raise
    except Exception as e:
        from app.config import setup_logging
        logger = setup_logging()
        logger.error(f"{DATABASE_ERROR_MSG} when updating character: {e}")
        raise HTTPException(status_code=500, detail=DATABASE_ERROR_MSG)


@router.delete("/character")
async def delete_character(
    name: str,
    db: Session = Depends(get_db_session)
):
    """Delete a character by name."""
    try:
        message = CharacterService.delete_character(name, db)
        return {"message": message}
    except HTTPException:
        raise
    except Exception as e:
        from app.config import setup_logging
        logger = setup_logging()
        logger.error(f"{DATABASE_ERROR_MSG} when deleting character: {e}")
        raise HTTPException(status_code=500, detail=DATABASE_ERROR_MSG)
