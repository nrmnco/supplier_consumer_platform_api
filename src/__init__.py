from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import select, Session
from src.models.cities import Cities
from src.core.database import create_db_and_tables
from src.routes import router
from src.core.database import engine

KZ_CITIES = [
    "Almaty",
    "Astana",
    "Shymkent",
    "Karaganda",
    "Aktobe",
    "Taraz",
    "Pavlodar",
    "Oskemen",
    "Semey",
    "Kyzylorda",
    "Atyrau",
    "Kostanay",
    "Petropavl",
    "Aktau",
    "Oral",
    "Temirtau",
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code here
    print("Starting up...")
    create_db_and_tables()

    with Session(engine) as session:
        count = session.exec(select(Cities)).first()

        if not count:
            for city in KZ_CITIES:
                city_instance = Cities(city_name=city)    
                session.add(city_instance)

            session.commit()
    yield
    print("Shutting down...")
    # Shutdown code here


app = FastAPI(lifespan=lifespan)

app.include_router(router)

@app.get("/")
async def read_root():
    return {"Hello": "World"}
