from src.Schemas.bookings import Booking
from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = Booking