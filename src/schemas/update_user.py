from sqlmodel import SQLModel
from enum import Enum


class UpdateUserSchema(SQLModel):
    first_name: str
    last_name: str
    phone_number: str

    email: str