from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship


class FileBase(SQLModel):
    id: int | None = Field(primary_key=True)
    filename: str = Field(nullable=False)
    front_name: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class File(FileBase, table=True):
    __tablename__ = "file"
    user_photo: "User" = Relationship(back_populates='photo')
