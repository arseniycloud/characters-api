"""Character service layer for business logic."""
from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.model import Character

# Constants
DATABASE_ERROR_MSG = "Database error"


class CharacterService:
    """Service for handling character business logic."""

    @staticmethod
    def get_all_characters(db: Session, skip: int = 0, limit: int = 100) -> List[Character]:
        """Get all characters with pagination."""
        return db.query(Character).offset(skip).limit(limit).all()

    @staticmethod
    def get_character_by_name(name: str, db: Session) -> Character:
        """Get character by name (case-insensitive)."""
        character = db.query(Character).filter(
            func.lower(Character.name) == name.lower()
        ).first()

        if not character:
            raise HTTPException(
                status_code=400,
                detail="Character with this name not found"
            )

        return character

    @staticmethod
    def create_character(character_data: dict, db: Session) -> Character:
        """Create a new character."""
        # Check if character already exists
        existing_character = db.query(Character).filter(
            func.lower(Character.name) == character_data["name"].lower()
        ).first()

        if existing_character:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Character with this name already exists. Please try using a different name.",
                    "name": character_data["name"]
                }
            )

        # Create new character
        try:
            new_character = Character(**character_data)
            db.add(new_character)
            db.commit()
            db.refresh(new_character)
            return new_character
        except Exception:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"{DATABASE_ERROR_MSG} when creating character")

    @staticmethod
    def update_character(character_data: dict, db: Session) -> Character:
        """Update an existing character."""
        character = db.query(Character).filter(
            func.lower(Character.name) == character_data["name"].lower()
        ).first()

        if not character:
            raise HTTPException(status_code=404, detail="Character not found for update")

        # Update fields
        try:
            for key, value in character_data.items():
                setattr(character, key, value)

            db.commit()
            db.refresh(character)
            return character
        except Exception:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"{DATABASE_ERROR_MSG} when updating character")

    @staticmethod
    def delete_character(name: str, db: Session) -> str:
        """Delete a character by name."""
        character = db.query(Character).filter(
            func.lower(Character.name) == name.lower()
        ).first()

        if not character:
            raise HTTPException(status_code=400, detail="Deletion not possible")

        try:
            db.delete(character)
            db.commit()
            return f"Character {name} deleted"
        except Exception:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"{DATABASE_ERROR_MSG} when deleting character")

    @staticmethod
    def check_db_connection(db: Session) -> bool:
        """Check database connection."""
        try:
            db.query(Character).first()
            return True
        except Exception:
            return False
