from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code here
    print("Starting up...")
    yield
    print("Shutting down...")
    # Shutdown code here

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def read_root():
    return {"Hello": "World"}