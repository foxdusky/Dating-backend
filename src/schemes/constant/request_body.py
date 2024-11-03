from typing import Literal

from sqlmodel import SQLModel


class GetALLRequestBody(SQLModel):
    limit: int | None = None
    offset: int | None = None
    sort_field: str | None = None
    sort_direction: Literal['asc', 'desc'] | None = None
    # In child class filter names as search_filter: ClassOfTheMainObject
