import uvicorn
from fastapi import FastAPI, Query, Body
import json

app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"}
]

@app.get("/hotels")
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
@app.put("/hotels/{hotel_id}")
def change_info(
        hotel_id: int,
        title: str = Body(embed = True),
        name: str = Body(embed = True)
):
    global hotels
    hotels[hotel_id-1]["title"] = title
    hotels[hotel_id-1]["name"] = name
    return {"status":"OK"}

@app.patch("hotels/{hotel_id}", summary = "Частичное обновление отеля")
def change_char(
        hotel_id: int,
        title: str | None = Body(embed = True),
        name: str | None = Body(embed = True)
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title is not None:
                hotel["title"] = title
            if name is not None:
                hotel["name"] = name
            return {"Status": "OK"}
    return {"error"}


    


#body, request body

@app.post("/hotels")
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
@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [ hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}

@app.get("/")
def func():
    return "Hello World!!!"


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)