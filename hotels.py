from fastapi import Query, Body, APIRouter

router = APIRouter(prefix  = "/hotels", tags = ["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"}
]

@router.get(
    "",
    summary = "Вывод отелей",
    description = "<h1>Введите айдишники отелей, которые хотите получить<h1>"
)
def get_hotels(
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
    return hotels_
@router.put(
    "/{hotel_id}",
    summary = "Полное изменение отелей",
    description = "<h1>Введите айдишник отеля, который хотите изменить и все данные для него<h1>"
)
def change_info(
        hotel_id: int,
        title: str = Body(embed = True),
        name: str = Body(embed = True)
):
    global hotels
    hotels[hotel_id-1]["title"] = title
    hotels[hotel_id-1]["name"] = name
    return {"status":"OK"}

@router.patch(
    "/{hotel_id}",
    summary = "Частичное изменение отелей",
    description = "<h1>Введите айдишник отеля, который хотите изменить и данные, которые хотите изменить<h1>"
)
def partially_edit_hotel(
        hotel_id: int,
        title: str | None = Body(None),
        name: str | None = Body(None),
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if title:
        hotel["title"] = title
    if name:
        hotel["name"] = name
    return {"status": "OK"}



#body, request body

@router.post(
    "",
    summary = "Добавление отелей",
    description = "<h1> Введите данные отеля, который хотите добавить <h1>"
)
def create_hotel(
        title: str = Body(embed = True),
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title
    })
    return {"status": "OK"}
#Body позволяет уйти от Query параметров (они не подходят для фунции - post,
#потому что отображаются в пути, в котором не должно быть информации о самом отеле)
@router.delete(
    "/{hotel_id}",
    summary = "Удаление отелей",
    description = "<h1>Введите айдишник отеля, который хотите удалить<h1>"
)
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}

