from typing import Annotated
from fastapi import Request, HTTPException

from fastapi import Depends, Query
from pydantic import BaseModel

from src.database import async_session_maker
from src.services.auth import AuthService
from src.utils.db_manager import DBManager


#class PaginationDep(BaseModel):
#    page: Annotated[int | None, Query(1, description = "Номер страницы", ge=1)]
#    per_page: Annotated[int | None, Query(None, description = "Количество отелей на страницу", ge = 1, le = 30)]

class PaginationParams(BaseModel):
    page: Annotated[int, Query(1, ge=1)]
    per_page: Annotated[int | None, Query(None, ge=1, lt=30)]

PaginationDep = Annotated[PaginationParams, Depends()]

def get_token(request: Request) -> str:
    token = access_token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(status_code=401, detail="Вы не предоставили токен доступа")
    return token

def get_curret_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().decode_token(token)
    return data["user_id"]

UserIdDep = Annotated[int, Depends(get_curret_user_id)]



async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db

DBDep = Annotated[DBManager, Depends(get_db)]







