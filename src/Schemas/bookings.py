from pydantic import BaseModel

from datetime import date

class BookingRequestAdd(BaseModel):
    room_id: int
    date_from: date
    date_to: date

class Booking(BookingRequestAdd):
    id: int
    user_id: int
    price: int
