from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from src.database import create_db_and_tables, get_session
from src.schemas.company import CompanyCreate
from sqlmodel import Session


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

@app.post("/test")
async def company_create(credentials: CompanyCreate, session: Session = Depends(get_session)):
    from src.cruds.company import company_create
    new_company = company_create(session, credentials)
    return new_company