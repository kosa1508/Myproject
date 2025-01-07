from fastapi import APIRouter, Body

from src.Schemas.rooms import RoomAdd
from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository

router = APIRouter(prefix = "/hotels", tags = ["Номера"])


@router.post(
    "/{hotel_id}/rooms",
    summary = "Добавление номеров",
    description = "<h1>Введите данные номера, который хотите добавить </h1>"
)
async def create_room(room_data: RoomAdd = Body(openapi_examples={
    "1":{"summary": "Люкс в Сочи", "value":{
        "hotel_id": 6,
        "title": "Люкс",
        "description": "Комфортабельный двухспальный номер с чудесном видом из окна",
        "price": 10000,
        "quantity": 5,
    }},
    "2":{"summary": "Апартаменты в Дубае", "value":{
        "hotel_id": 7,
        "title": "Апартаменты",
        "description": "",
        "price": 25000,
        "quantity": 30,
    }}
})
):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data)
        await session.commit()

    return {"status": "OK", "data": room}








