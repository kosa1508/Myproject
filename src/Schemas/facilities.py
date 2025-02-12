from pydantic import BaseModel, ConfigDict

class FacilityAdd(BaseModel):
    title: str

class Facility(BaseModel):
    id: int
    title: str

    model_config = ConfigDict(from_attributes=True)