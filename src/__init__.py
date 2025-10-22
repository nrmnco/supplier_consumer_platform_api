from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code here
    print("Starting up...")
    create_db_and_tables()
    yield
    print("Shutting down...")
    # Shutdown code here

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def read_root():
    return {"Hello": "World"}