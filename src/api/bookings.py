from fastapi import APIRouter, Body

from src.Schemas.bookings import BookingRequestAdd, Booking, BookingAdd
from src.api.dependencies import DBDep, UserIdDep

router = APIRouter(prefix = "/bookings", tags = ["Бронирование отелей"])

@router.post(
    "",
    summary = "Добавление бронирований",
    description = "<h1>Введите данные необходимые для бронирования</h1>"
)
async def add_booking(
        db: DBDep,
        user_id: UserIdDep,
        booking_data: BookingRequestAdd = Body(openapi_examples={
    "1":{"summary":"Бронь 1", "value":{
        "room_id": 4,
        "date_from": "2024-01-08",
        "date_to": "2024-01-15"
    }},
    "2":{"summary": "Бронь 2", "value":{
        "room_id": 5,
        "date_from": "2024-01-05",
        "date_to": "2024-01-14"
    }}
})
):
    # Получить цену номера
    # Создать схему данных BookingAdd
    # Добавить бронирование конкретному пользователю
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    room_price: int = room.price
    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump()
    )
    booking = await db.bookings.add(_booking_data)
    await db.commit()

    return {"status": "OK", "data": booking}

@router.get(
    "",
    summary="Получение всех бронирований",
    description="<h1>Все бронирования</h1>"
)

async def get_bookings(
    db: DBDep,
):
    return await db.bookings.get_all()

@router.get(
    "/me",
    summary="Получение бронирований конкретного пользователя",
    description="<h1>Ваши бронирования</h1>"
)

async def get_booking(
    db: DBDep,
    user_id: UserIdDep,
):
    return await db.bookings.get_filtered(user_id=user_id)