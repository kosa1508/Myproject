from sqlalchemy import select, func

from src.Schemas.rooms import Room
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm

class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

