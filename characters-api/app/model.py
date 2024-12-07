from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# Определение модели Character для базы данных
class Character(Base):
    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    education = Column(String, nullable=True)
    height = Column(Integer, nullable=True)
    identity = Column(String, nullable=True)
    other_aliases = Column(String, nullable=True)
    universe = Column(String, nullable=True)
    weight = Column(Integer, nullable=True)
