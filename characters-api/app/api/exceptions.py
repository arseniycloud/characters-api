"""Custom API exceptions."""
from fastapi import HTTPException


class CharacterNotFoundError(HTTPException):
    """Exception raised when character is not found."""
    def __init__(self, detail: str = "Character not found"):
        super().__init__(status_code=404, detail=detail)


class CharacterAlreadyExistsError(HTTPException):
    """Exception raised when character already exists."""
    def __init__(self, character_name: str):
        super().__init__(
            status_code=400,
            detail={
                "message": "Character with this name already exists. Please try using a different name.",
                "name": character_name
            }
        )
