from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship


class UserBase(SQLModel):
    id: int | None = Field(primary_key=True)
    username: str = Field(nullable=False)
    password: str = Field(nullable=False)
    e_mail: str = Field(nullable=False, unique=True)
    name: str | None
    surname: str | None
    profile_photo: int | None = Field(foreign_key='file.id')
    gender: int = Field(nullable=False, foreign_key='gender.id')
    reg_at: datetime = Field(default_factory=datetime.utcnow)


class User(UserBase, table=True):
    __tablename__ = "user"
    gender: "Gender" = Relationship(back_populates='users')
    photo: "File" = Relationship(back_populates="user_photo")
