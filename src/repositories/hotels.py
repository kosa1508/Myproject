from sqlalchemy import select, func

from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(
            self,
            location,
            title,
            limit,
            offset,
    ):
        query = select(HotelsOrm)

        if location:
            query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))
        if title:
            query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))

        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        print(query.compile(compile_kwargs={"literal_bings": True}))
        result = await self.session.execute(query)

        return result.scalars().all()

#class ONEHotelRepository(BaseRepository):
#    model = HotelsOrm
 #   async def get_one(
  #          self,
   #         location,
    #        title,
#    ):
 #
  #      query = select(HotelsOrm)
   #
    #    if location:
     #       query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))
      #  if title:
  #          query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))
   #
    #    result = await self.session.execute(query)

     #   return result.scalars().all()