"""FastAPI dependencies."""
from functools import lru_cache
from sqlalchemy.orm import Session

from app.configdb import get_db


def get_db_session() -> Session:
    """Get database session dependency."""
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()
