from fastapi import APIRouter, Body

from src.Schemas.bookings import BookingRequestAdd, Booking
from src.api.dependencies import DBDep, UserIdDep

router = APIRouter(prefix = "/bookings", tags = ["Бронирование отелей"])

@router.post(
    "",
    summary = "Добавление бронирований",
    description = "<h1>Введите данные необходимые для бронирования</h1>"
)
async def create_booking(
        db: DBDep,
        user_id: UserIdDep,
        booking_data: BookingRequestAdd = Body(openapi_examples={
    "1":{"summary":"Бронь 1", "values":{
        "room_id": 4,
        "date_from": "2024-01-08",
        "date_to": "2024-01-15"
    }},
    "2":{"summary": "Бронь 2", "values":{
        "room_id": 5,
        "date_from": "2024-01-05",
        "date_to": "2024-01-14"
    }}
})
):
    room = await db.rooms.get_filtered(id=booking_data.room_id)
    user = await db.users.get_one_or_none(id=user_id)
    _booking_data = Booking(room_id=room.id, user_id=user.id, price=room.price, **booking_data.model_dump())
    booking = await db.bookings.add(_booking_data)
    await db.commit()

    return {"status": "OK", "data": room}