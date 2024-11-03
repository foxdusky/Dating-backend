from datetime import datetime

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


class UserSearchFilter(SQLModel):
    id: int | None = None
    username: str | None = None
    e_mail: str | None = None
    name: str | None = None
    surname: str | None = None
    gender_id: int | None = None
    reg_at: datetime | None = None


class UserListRequestBody(GetALLRequestBody):
    search_filter: UserSearchFilter | None = None
    distance_filter: float | None = None


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
