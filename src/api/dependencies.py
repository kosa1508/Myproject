from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(None, description = "Номер страницы", ge=1)]
    per_page: Annotated[int | None, Query(None, description = "Количество отелей на страницу", ge = 1, le = 30)]