from sqlmodel import SQLModel

class LinkingSchema(SQLModel):
    message: str
    