from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.core.database import create_db_and_tables
from src.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code here
    print("Starting up...")
    create_db_and_tables()
    yield
    print("Shutting down...")
    # Shutdown code here


app = FastAPI(lifespan=lifespan)

app.include_router(router)

@app.get("/")
async def read_root():
    return {"Hello": "World"}
