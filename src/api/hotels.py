from datetime import date

from fastapi import Query, APIRouter, Body, Depends

from src.Schemas.hotels import HotelPATCH, HotelAdd
from src.api.dependencies import PaginationDep, DBDep


router = APIRouter(prefix  = "/hotels", tags = ["Отели"])

@router.get(
    "",
    summary="Вывод отелей",
    description="<h1>Вот все отели, свободные в данный промежуток времени</h1>"
)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    location: str | None = Query(None, description="Локация"),
    title: str | None = Query(None, description="Название отеля"),
    date_from:date = Query(example="2025-01-01"),
    date_to: date = Query(example="2025-03-03"),
):
    per_page = pagination.per_page or 5
    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        limit=per_page or 5,
        offset=per_page * (pagination.page - 1)
    )
   # return await db.hotels.get_all(
    #location=location,
    #title=title,
    #limit=per_page or 5,
    #offset=per_page * (pagination.page - 1)
    #)



@router.put(
    "/{hotel_id}",
    summary = "Полное изменение отеля",
    description = "<h1>Введите айдишник отеля, который хотите изменить, и все данные для него</h1>"
)
async def edit_hotel(
        hotel_id: int,
        hotel_data: HotelAdd,
        db:DBDep
):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status":"OK"}


@router.get("/{hotel_id}",)
async def get_hotel(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post(
    "",
    summary = "Добавление отелей",
    description = "<h1> Введите данные отеля, который хотите добавить </h1>"
)
async def create_hotel(db: DBDep, hotel_data: HotelAdd = Body(openapi_examples={
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
    hotel = await  db.hotels.add(hotel_data)
    await db.commit()

    return {"status": "OK", "data": hotel}
#Body позволяет уйти от Query параметров (они не подходят для фунции - post,
#потому что отображаются в пути, в котором не должно быть информации о самом отеле)

@router.patch(
    "/{hotel_id}",
    summary = "Частичное изменение отелей",
    description = "<h1>Введите айдишник отеля, который хотите изменить и данные, которые хотите изменить</h1>"
)
async def partially_edit_hotel(hotel_id: int, hotel_data: HotelPATCH, db:DBDep):
    #global hotels
    #hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    #if hotel_data.title:
    #    hotel["title"] = hotel_data.title
    #if hotel_data.name:
    #    hotel["name"] = hotel_data.name
    await db.hotels.edit(hotel_data, exclude_unset = True,  id=hotel_id)
    await db.commit()
    return {"status": "OK"}

#body, request body

@router.delete(
    "/{hotel_id}",
    summary = "Удаление отелей",
    description = "<h1>Введите айдишник отеля, который хотите удалить</h1>"
)
async def delete_hotel(hotel_id: int, db: DBDep):
    #global hotels
    #hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    #return {"status": "OK"}

    await db.hotels.delete(id=hotel_id)
    await db.commit()

    return {"status": "OK"}


