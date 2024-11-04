from typing import Literal, Optional

from sqlmodel import SQLModel, Field


class GetALLRequestBody(SQLModel):
    limit: Optional[int] = Field(
        description="Limit of returning exemplars"
    )
    offset: Optional[int] = Field(
        description="Offset of returning exemplars"
    )
    sort_field: Optional[int] = Field(
        description="Field name for sorting, like an name of parameters in search filter"
    )
    sort_direction: Literal['asc', 'desc'] | None = None
    # In child class filter names as search_filter: ClassOfTheMainObject
