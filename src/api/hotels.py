from fastapi import Query, APIRouter, Body, Depends
from typing import Annotated

from src.Schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationParams

router = APIRouter(prefix  = "/hotels", tags = ["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]

@router.get(
    "",
    summary = "Вывод отелей",
    description = "<h1>Введите айдишники отелей, которые хотите получить<h1>"
)
def get_hotels(
        pagination: Annotated[PaginationParams, Depends()],
        id:int | None = Query(None, description = "Айдишник"),
        title: str | None = Query(None, description = "Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    if page and per_page:
        return hotels_[per_page*(page-1):][:per_page]
    return hotels_

@router.put(
    "/{hotel_id}",
    summary = "Полное изменение отелей",
    description = "<h1>Введите айдишник отеля, который хотите изменить и все данные для него<h1>"
)
def change_info(hotel_id: int, hotel_data: Hotel):
    global hotels
    hotels[hotel_id-1]["title"] = hotel_data.title
    hotels[hotel_id-1]["name"] = hotel_data.name
    return {"status":"OK"}

@router.post(
    "",
    summary = "Добавление отелей",
    description = "<h1> Введите данные отеля, который хотите добавить <h1>"
)
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1":{"summary": "Сочи", "value":{
            "title": "Отель Сочи 5 звезд у моря",
            "name": "sochi_u_morya",
        }},
    "2":{"summary": "Дубай", "value":{
            "title": "Отель Дубай у фонтана",
            "name": "dubai_fontain",
        }}
})
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name,
    })
    return {"status": "OK"}
#Body позволяет уйти от Query параметров (они не подходят для фунции - post,
#потому что отображаются в пути, в котором не должно быть информации о самом отеле)

@router.patch(
    "/{hotel_id}",
    summary = "Частичное изменение отелей",
    description = "<h1>Введите айдишник отеля, который хотите изменить и данные, которые хотите изменить<h1>"
)
def partially_edit_hotel(hotel_id: int, hotel_data: HotelPATCH):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.title:
        hotel["title"] = hotel_data.title
    if hotel_data.name:
        hotel["name"] = hotel_data.name
    return {"status": "OK"}

#body, request body

@router.delete(
    "/{hotel_id}",
    summary = "Удаление отелей",
    description = "<h1>Введите айдишник отеля, который хотите удалить<h1>"
)
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}

