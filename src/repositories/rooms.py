from sqlalchemy import select, func

from src.Schemas.rooms import Room
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm

class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_all(
            self,
            hotel_id: int,
            title,
            description,
            price,
            quantity
    ) -> list[Room]:
        query = select(RoomsOrm)

        if hotel_id:
            query.filter(func.lower(RoomsOrm.hotel_id).contains(hotel_id.strip().lower()))
        if title:
            query.filter(func.lower(RoomsOrm.title).contains(title.strip().lower()))
        if description:
            query.filter(func.lower(RoomsOrm.description).contains(description.strip().lower()))
        if price:
            query.filter(func.lower(RoomsOrm.price).contains(price.strip().lower()))
        if quantity:
            query.filter(func.lower(RoomsOrm.quantity).contains(quantity.strip().lower()))


        print(query.compile(compile_kwargs={"literal_bings": True}))
        result = await self.session.execute(query)

        return [Room.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]

