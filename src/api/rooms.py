from fastapi import APIRouter, Body, Query

from datetime import date

from src.Schemas.facilities import RoomFacilityAdd
from src.Schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch, Room
from src.api.dependencies import DBDep

router = APIRouter(prefix = "/hotels", tags = ["Номера"])

@router.get(
    "/{hotel_id}/rooms",
    summary = "Получение номеров определенного отеля",
    description = "Вот все ваши номера"
)
async def get_rooms(
        hotel_id: int,
        db: DBDep,
        date_from: date = Query(example="2025-01-01"),
        date_to: date = Query(example="2025-03-03")
):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)

@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post(
    "/{hotel_id}/rooms",
    summary = "Добавление номеров",
    description = "<h1>Введите данные номера, который хотите добавить </h1>"
)
async def create_room(db: DBDep, hotel_id: int, room_data: RoomAddRequest = Body(openapi_examples={
    "1":{"summary": "Люкс в Сочи", "value":{
        "title": "Люкс",
        "description": "Комфортабельный двухспальный номер с чудесном видом из окна",
        "price": 10000,
        "quantity": 5,
        "facilities_ids": 1
    }},
    "2":{"summary": "Апартаменты в Дубае", "value":{
        "title": "Апартаменты",
        "description": "",
        "price": 25000,
        "quantity": 30,
        "facilities_ids": "2"
    }}
})
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)

    rooms_facilities_data = [RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()

    return {"status": "OK", "data": room}

@router.put(
    "/{hotel_id}/rooms/{room_id}",
    summary = "Полное изменение номера",
    description = "<h1>Введите айдишник номера, который хотите изменить, и все необходимые данные</h1>"
)
async def edit_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomAddRequest):
    await db.rooms_facilities.delete(room_id=room_id)
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, id=room_id)

    rooms_facilities_data = [RoomFacilityAdd(room_id=room_id, facility_id=f_id) for f_id in room_data.facilities_ids]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()


    return {"status": "OK", "data": _room_data}

@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary = "Частичное изменение номера",
    description = "<h1>Введите айдишник номера, который хотите изменить, и данные для изменения</h1>"
)
async def partially_edit_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest,
        db: DBDep
):
    _room_data_facilities = RoomPatchRequest(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    if _room_data_facilities.facilities_ids:
        await db.rooms_facilities.delete(room_id=room_id)
        rooms_facilities_data = [RoomFacilityAdd(room_id=room_id, facility_id=f_id) for f_id in room_data.facilities_ids]
        await db.rooms_facilities.add_bulk(rooms_facilities_data)
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset = True))
    await db.rooms.edit(_room_data, exclude_unset = True, id = room_id, hotel_id = hotel_id)
    await db.commit()
    return {"status": "OK", "data": _room_data}

@router.delete(
    "/{hotel_id}/rooms/{room_id}",
    summary = "Удаление номера",
    description = "Введите айдишник номера, который хотите удалить"
)
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}






