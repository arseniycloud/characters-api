from typing import Optional

from pydantic import BaseModel, Field


class CharacterCreate(BaseModel):
    """Модель данных для создания нового персонажа."""
    name: str = Field(..., min_length=1, max_length=50, description="Name of the character")
    education: Optional[str] = Field(None, description="Education of the character")
    height: Optional[float] = Field(None, ge=0, description="Height of the character in meters")
    identity: Optional[str] = Field(None, description="Identity of the character")
    other_aliases: Optional[str] = Field(None, description="Other aliases of the character")
    universe: Optional[str] = Field(None, description="Universe of the character")
    weight: Optional[float] = Field(None, ge=0, description="Weight of the character in kilograms")

    class Config:
        orm_mode = True


class CharacterResponse(BaseModel):
    """Модель данных для ответа без идентификатора."""
    name: str
    education: Optional[str] = None
    height: Optional[float] = None
    identity: Optional[str] = None
    other_aliases: Optional[str] = None
    universe: Optional[str] = None
    weight: Optional[float] = None

    class Config:
        orm_mode = True


# Определяем модель данных для запроса
class GenerateRequest(BaseModel):
    prompt: str = "Most beautiful place in the word"
