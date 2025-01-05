from fastapi import Query, APIRouter, Body, Depends

from sqlalchemy import insert, select, func

from typing import Annotated

from src.Schemas.hotels import Hotel, HotelPATCH, HotelAdd
from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.models.hotels import HotelsOrm
from src.repositories.hotels import HotelsRepository

router = APIRouter(prefix  = "/hotels", tags = ["Отели"])


@router.get(
    "",
    summary = "Вывод отелей",
    description = "<h1>Введите айдишники отелей, которые хотите получить<h1>"
)
async def get_hotels(
        pagination: PaginationDep,
        location: str | None = Query(None, description = "Локация"),
        title: str | None = Query(None, description = "Название отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page or 5,
            offset=per_page * (pagination.page - 1)
        )


    #per_page = pagination.per_page or 5

    #async with async_session_maker() as session:
    #   query = select(HotelsOrm)

    #    if location:
    #        query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))
    #    if title:
    #        query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))

    #    query = (
    #        query
    #        .limit(per_page)
    #        .offset(per_page * (pagination.page - 1))
    #    )

    #    print(query.compile(compile_kwargs={"literal_bings": True}))
    #    result = await session.execute(query)
    #    hotels = result.scalars().all()
    #    print(type(hotels), hotels)
    #    return hotels


        #hotels = result.all() - сохраняет в переменную и выводит все отели
        #first_hotel = result.first() - сохраняет и выводит только первый объект(отель)
        #result.one() - проверяет и выводит конкретно 1 какой-то отель
        #result.one_or_none() - проверяет и выводит конкретно 1 или ноль отелей

    #if page and per_page:
    #return hotels_[per_page*(page-1):][:per_page]


@router.put(
    "/{hotel_id}",
    summary = "Полное изменение отелей",
    description = "<h1>Введите айдишник отеля, который хотите изменить и все данные для него<h1>"
)
async def edit_hotel(hotel_id: int, hotel_data: HotelAdd):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
    return {"status":"OK"}


@router.get("/{hotel_id}",)
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)


@router.post(
    "",
    summary = "Добавление отелей",
    description = "<h1> Введите данные отеля, который хотите добавить <h1>"
)
async def create_hotel(hotel_data: HotelAdd = Body(openapi_examples={
    "1":{"summary": "Сочи", "value":{
            "title": "Отель Сочи 5 звезд у моря",
            "location": "ул. Моря, 1",
        }},
    "2":{"summary": "Дубай", "value":{
            "title": "Отель Дубай у фонтана",
            "location": "ул. Шейха, 2",
        }}
})
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "OK", "data": hotel}
#Body позволяет уйти от Query параметров (они не подходят для фунции - post,
#потому что отображаются в пути, в котором не должно быть информации о самом отеле)

@router.patch(
    "/{hotel_id}",
    summary = "Частичное изменение отелей",
    description = "<h1>Введите айдишник отеля, который хотите изменить и данные, которые хотите изменить<h1>"
)
async def partially_edit_hotel(hotel_id: int, hotel_data: HotelPATCH):
    #global hotels
    #hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    #if hotel_data.title:
    #    hotel["title"] = hotel_data.title
    #if hotel_data.name:
    #    hotel["name"] = hotel_data.name
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, exclude_unset = True,  id=hotel_id)
        await session.commit()
    return {"status": "OK"}

#body, request body

@router.delete(
    "/{hotel_id}",
    summary = "Удаление отелей",
    description = "<h1>Введите айдишник отеля, который хотите удалить<h1>"
)
async def delete_hotel(hotel_id: int):
    #global hotels
    #hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    #return {"status": "OK"}

    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()

    return {"status": "OK"}


