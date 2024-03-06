from uuid import UUID
from pydantic import BaseModel, ConfigDict


class Hotel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    image_url: str
    city: str
    description: str


class CreateHotelRequest(BaseModel):
    name: str
    image_url: str
    city: str
    description: str