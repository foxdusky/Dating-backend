from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship


class MatchingBase(SQLModel):
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    liked_user_id: int = Field(foreign_key="user.id", primary_key=True)
    is_mutual: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Matching(MatchingBase, table=True):
    __tablename__ = "matching"
