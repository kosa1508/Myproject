from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel


#class PaginationDep(BaseModel):
#    page: Annotated[int | None, Query(1, description = "Номер страницы", ge=1)]
#    per_page: Annotated[int | None, Query(None, description = "Количество отелей на страницу", ge = 1, le = 30)]

class PaginationParams(BaseModel):
    page: Annotated[int, Query(1, ge=1)]
    per_page: Annotated[int | None, Query(None, ge=1, lt=30)]

PaginationDep = Annotated[PaginationParams, Depends()]