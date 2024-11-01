from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship


class GenderBase(SQLModel):
    id: int | None = Field(primary_key=True)
    name: str = Field(unique=True, nullable=False)


class Gender(GenderBase, table=True):
    __tablename__ = "gender"
    users: ["User"] = Relationship(back_populates='gender')
