from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship


class UserBase(SQLModel):
    id: int | None = Field(primary_key=True, default=None)
    username: str | None = Field(nullable=False)
    password: str | None = Field(nullable=False)
    e_mail: str | None = Field(nullable=False, unique=True)
    name: str | None = Field()
    surname: str | None = Field()
    profile_photo: int | None = Field(foreign_key='file.id', default=None)
    gender_id: int | None = Field(nullable=False, foreign_key='gender.id')
    reg_at: datetime | None = Field(default_factory=datetime.utcnow)


class User(UserBase, table=True):
    __tablename__ = "user"
    gender: "Gender" = Relationship(back_populates='users')
    photo: "File" = Relationship(back_populates="user_photo")


from schemes.user.gender_scheme import Gender
from schemes.file.file_scheme import File
