from sqlmodel import SQLModel, Field

class Cities(SQLModel, table=True):
    __tablename__ = "cities"

    city_id: int | None = Field(primary_key=True, default=None)
    city_name: str = Field(unique=True, nullable=False)