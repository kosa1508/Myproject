from fastapi import APIRouter, Body

from src.Schemas.rooms import RoomAdd, RoomAddRequest
from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository

router = APIRouter(prefix = "/hotels", tags = ["Номера"])

@router.get(
    "/{hotel_id}/rooms",
    summary = "Получение номеров определенного отеля",
    description = "Вот все ваши номера"
)
async def get_rooms():
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all()

@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id)


@router.post(
    "/{hotel_id}/rooms",
    summary = "Добавление номеров",
    description = "<h1>Введите данные номера, который хотите добавить </h1>"
)
async def create_room(hotel_id: int, room_data: RoomAddRequest = Body(openapi_examples={
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
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(_room_data)
        await session.commit()

    return {"status": "OK", "data": room}

@router.put(
    "/{hotel_id}/rooms/{room_id}",
    summary = "Полное изменение номера",
    description = "<h1>Введите айдишник номера, который хотите изменить, и все необходимые данные</h1>"
)
async def edit_room(room_id, room_data: RoomAdd):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, id=room_id)
        await session.commit()
    return {"status": "OK"}







