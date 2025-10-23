from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from sqlmodel import Session
from src.core.database import create_db_and_tables, get_session
from src.routes.authentication import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code here
    print("Starting up...")
    create_db_and_tables()
    yield
    print("Shutting down...")
    # Shutdown code here


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)

@app.get("/")
async def read_root():
    return {"Hello": "World"}
