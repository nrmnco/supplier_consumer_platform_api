from sqlmodel import create_engine, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker
from src.config import settings

DATABASE_URL = f"postgresql+psycopg2://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

engine = create_engine(DATABASE_URL, echo=True)

# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)

SQLModel.metadata.create_all(engine)
