from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlmodel import select, Session
from src.models.cities import Cities
from src.core.database import create_db_and_tables
from src.routes import router
from src.core.database import engine
from src.core.middleware import log_middleware

KZ_CITIES = [
    {"en": "Almaty",      "ru": "Алматы",      "kz": "Алматы"},
    {"en": "Astana",      "ru": "Астана",      "kz": "Астана"},
    {"en": "Shymkent",    "ru": "Шымкент",     "kz": "Шымкент"},
    {"en": "Karaganda",   "ru": "Караганда",   "kz": "Қарағанды"},
    {"en": "Aktobe",      "ru": "Актобе",      "kz": "Ақтөбе"},
    {"en": "Taraz",       "ru": "Тараз",       "kz": "Тараз"},
    {"en": "Pavlodar",    "ru": "Павлодар",    "kz": "Павлодар"},
    {"en": "Oskemen",     "ru": "Усть-Каменогорск", "kz": "Өскемен"},
    {"en": "Semey",       "ru": "Семей",       "kz": "Семей"},
    {"en": "Kyzylorda",   "ru": "Кызылорда",   "kz": "Қызылорда"},
    {"en": "Atyrau",      "ru": "Атырау",      "kz": "Атырау"},
    {"en": "Kostanay",    "ru": "Костанай",    "kz": "Қостанай"},
    {"en": "Petropavl",   "ru": "Петропавловск", "kz": "Петропавл"},
    {"en": "Aktau",       "ru": "Актау",       "kz": "Ақтау"},
    {"en": "Oral",        "ru": "Уральск",     "kz": "Орал"},
    {"en": "Temirtau",    "ru": "Темиртау",    "kz": "Теміртау"},
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
                city_instance = Cities(
                    city_name=city["en"],
                    city_name_ru=city["ru"],
                    city_name_kz=city["kz"],
                )
                session.add(city_instance)

            session.commit()
    yield
    print("Shutting down...")
    # Shutdown code here


app = FastAPI(lifespan=lifespan)
app.middleware("http")(log_middleware)

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
    ],
    allow_origin_regex="https?://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

