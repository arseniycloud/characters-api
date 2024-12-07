import json
from typing import Dict, List

import requests
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel, Field
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.config import setup_logging
from app.configdb import get_db
from app.model import Character
from app.schemas import CharacterResponse, GenerateRequest

# Настройка логирования
logger = setup_logging()

# Инициализация приложения FastAPI
app = FastAPI()
Instrumentator().instrument(app).expose(app)


# Определение Pydantic модели
class CharacterCreate(BaseModel):
    name: str = Field(..., min_length=1, description="Имя персонажа, должно содержать хотя бы один символ")
    universe: str
    weight: float = Field(..., description="Вес персонажа, должен быть числом")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Обработчик исключений для ошибок валидации запросов."""
    return JSONResponse(
        status_code=400,
        content={"detail": exc.errors()},
    )


# Маршруты
@app.get("/")
async def read_root():
    """Приветственное сообщение корневого маршрута."""
    return {"message": "Welcome to my FastAPI application!"}


@app.get("/characters", response_model=Dict[str, List[CharacterResponse]])
async def get_all_characters(db: Session = Depends(get_db)):
    """Получить список всех персонажей."""
    characters = db.query(Character).all()
    return {"result": characters}


@app.get("/character", response_model=Dict[str, CharacterResponse])
async def get_character_by_name(name: str, db: Session = Depends(get_db)):
    """Получить персонажа по имени."""
    character = db.query(Character).filter(func.lower(Character.name) == name.lower()).first()
    if character:
        return {"result": character}
    raise HTTPException(status_code=400, detail="Character with this name not found")


@app.post("/character", status_code=200, response_model=Dict[str, CharacterResponse])
async def create_character(character_data: CharacterCreate, db: Session = Depends(get_db)):
    """Создать нового персонажа."""
    try:
        # Проверка на существование персонажа с таким именем
        existing_character = db.query(Character).filter(
            func.lower(Character.name) == character_data.name.lower()).first()
        if existing_character:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Character with this name already exists. Please try using a different name.",
                    "name": character_data.name
                }
            )

        # Создание нового персонажа
        new_character = Character(**character_data.dict())
        db.add(new_character)
        db.commit()
        db.refresh(new_character)

        return {"result": new_character}
    except SQLAlchemyError as e:
        logger.error(f"Ошибка базы данных при создании персонажа: {e}")
        raise HTTPException(status_code=500, detail="Ошибка базы данных")


@app.put("/character", response_model=Dict[str, CharacterResponse])
async def update_character(character_data: CharacterCreate, db: Session = Depends(get_db)):
    """Обновить существующего персонажа."""
    try:
        character = db.query(Character).filter(
            func.lower(Character.name) == character_data.name.lower()).first()
        if not character:
            raise HTTPException(status_code=404, detail="Персонаж для обновления не найден")

        for key, value in character_data.dict(exclude_unset=True).items():
            setattr(character, key, value)

        db.commit()
        db.refresh(character)

        return {"result": character}
    except SQLAlchemyError as e:
        logger.error(f"Ошибка базы данных при обновлении персонажа: {e}")
        raise HTTPException(status_code=500, detail="Ошибка базы данных")


@app.delete("/character")
async def delete_character(name: str, db: Session = Depends(get_db)):
    """Удалить персонажа по имени."""
    character = db.query(Character).filter(func.lower(Character.name) == name.lower()).first()
    if not character:
        raise HTTPException(status_code=400, detail="Deletion not possible")

    db.delete(character)
    db.commit()

    return {"message": f"Character {name} deleted"}


@app.get("/test-db")
async def test_db(db: Session = Depends(get_db)):
    """Проверить соединение с базой данных."""
    try:
        db.query(Character).all()
        return {"status": "Database connection successful"}
    except SQLAlchemyError as e:
        logger.error(f"Ошибка базы данных при тестировании соединения: {e}")
        return {"status": "Database error", "details": str(e)}


@app.post("/generate-ai-text")
async def generate_ai_text(request_data: GenerateRequest):
    try:
        payload = {
            "model": "llama3",
            "prompt": request_data.prompt + "Дай ответ на русском языке",
            "stream": False
        }

        # Отправляем запрос на локальный API для генерации текста
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload
        )

        response.raise_for_status()

        # Получаем и обрабатываем ответ от API
        api_response = response.json()
        formatted_response = api_response['response']

        # Возвращаем отформатированный ответ без спецсимволов
        return formatted_response
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Ошибка связи с сервером: {str(e)}")


@app.post("/generate-ai-json")
async def generate_ai_json(request_data: GenerateRequest):
    try:
        payload = {
            "model": "llama3",
            "prompt": request_data.prompt + "Дай ответ в виде JSON на русском языке",
            "format": "json",
            "stream": False
        }

        # Отправляем запрос на локальный API для генерации текста
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload
        )

        response.raise_for_status()
        # Получаем и обрабатываем ответ от API
        api_response = response.json()
        formatted_response = json.loads(api_response['response'])

        # Возвращаем отформатированный ответ без спецсимволов
        return formatted_response
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Ошибка связи с сервером: {str(e)}")
