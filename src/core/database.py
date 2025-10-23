from sqlmodel import create_engine, SQLModel, Session
from src.core.config import settings

# DATABASE_URL = f"postgresql+psycopg2://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
DATABASE_URL = f"postgresql+psycopg2://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@localhost:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    from src.models import chats, messages, users, companies, linkings, products, orders, order_products, complaint_history, complaints
    SQLModel.metadata.create_all(engine)

# SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
