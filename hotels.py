from fastapi import Query, APIRouter, Body

from Schemas.hotels import Hotel, HotelPATCH

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
        id:int | None = Query(None, description = "Айдишник"),
        title: str | None = Query(None, description = "Название отеля"),
        page:int | None = Query(None, description = "Номер страницы"),
        per_page:int | None = Query(None, description = "Количество отелей на страницу"),
):
    hotels_ = []
    if not id and not title and not per_page:
        hotels_ = hotels
    elif not id and not title and per_page and not page:
        for i in range(per_page):
            for hotel in hotels:
                if hotel["id"] == i+1:
                    hotels_.append(hotel)
    elif not id and not title and per_page and page:
        j = (page - 1) * per_page + 1
        for i in range(j, per_page*page+1):
            for hotel in hotels:
                if hotel["id"] == i:
                    hotels_.append(hotel)
    else:
        for hotel in hotels:
            if id and hotel["id"] != id:
                continue
            if title and hotel["title"] != title:
                continue
            hotels_.append(hotel)

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

