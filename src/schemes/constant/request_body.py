from typing import Literal

from sqlmodel import SQLModel, Field


class GetALLRequestBody(SQLModel):
    limit: int | None = Field(
        description="Limit of returning exemplars"
    )
    offset: int | None = Field(
        description="Offset of returning exemplars"
    )
    sort_field: str | None = Field(
        description="Field name for sorting, like an name of parameters in search filter"
    )
    sort_direction: Literal['asc', 'desc'] | None = None
    # In child class filter names as search_filter: ClassOfTheMainObject
