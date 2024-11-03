from datetime import datetime
from typing import Annotated

from fastapi import Form
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship

from schemes.constant.request_body import GetALLRequestBody


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
    longitude: float | None = Field()
    width: float | None = Field()


class User(UserBase, table=True):
    __tablename__ = "user"
    gender: "Gender" = Relationship(back_populates='users')
    photo: "File" = Relationship(back_populates="user_photo")


class UserRegistration(BaseModel):
    username: str = Field(description="Require a unique name of user, also it's checking for unique")
    password: str
    e_mail: str = Field(description="Require a user email, also it's checking for unique")
    name: str | None = None
    surname: str | None = None
    gender_id: int = Field(description="Users gender in int 1 is male, 2 is female")
    width: float | None = None
    longitude: float | None = None

    class Config:
        title = "User Registration Body"
        schema_extra = {
            "example": {
                "username": "example_user",
                "password": "example_password",
                "e_mail": "user@example.com",
                "name": "John",
                "surname": "Doe",
                "gender_id": 1,
                "width": 180.5,
                "longitude": -75.0
            }
        }


class UserSearchFilter(SQLModel):
    id: int | None = None
    username: str | None = None
    e_mail: str | None = None
    name: str | None = None
    surname: str | None = None
    gender_id: int | None = None
    reg_at: datetime | None = None


class UserListRequestBody(GetALLRequestBody):
    search_filter: UserSearchFilter | None = Field(
        description="Search filter by columns, insert any value in params to get filtered result"
    )
    distance_filter: float | None = Field(
        description="Distance filter, require float value in kilometers"
    )


class UserInfo(SQLModel):
    id: int
    username: str
    e_mail: str
    name: str | None = None
    surname: str | None = None
    reg_at: datetime
    gender: "Gender"
    photo: "File"


class UserResponseAll(SQLModel):
    count: int
    result: list[UserInfo]


from schemes.user.gender_scheme import Gender
from schemes.file.file_scheme import File

UserInfo.model_rebuild()
UserResponseAll.model_rebuild()
