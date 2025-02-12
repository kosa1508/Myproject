from fastapi import APIRouter, Body

from src.Schemas.facilities import FacilityAdd
from src.api.dependencies import DBDep


router = APIRouter(prefix = "/facilities", tags = ["Удобства предоставленные отелями"])

@router.post(
    "",
    summary = "Добавление удобств",
    description = "<h1>Введите название нового удобства<h1>",
)

async def add_facility(
    db: DBDep,
    facility_data: FacilityAdd = Body(openapi_examples={
        "1":{"summary": "Интернет", "value":{
                "title": "Бесплатный интернет",
            }},
        "2":{"summary": "Сауна", "value":{
                "title": "Наличие сауны",
            }}
})

):
    facility = await db.facilities.add(facility_data)

    await db.commit()

    return {"status": "OK", "data": facility}

@router.get(
    "",
    summary = "Получение всех удобств",
    description = "<h1>Вот все доступные в отелях удобства<h1>"
)
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()

