from uuid import UUID
from pydantic import BaseModel, ConfigDict


class Booking(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    user_id: UUID
    hotel_id: UUID
    price: str
    resident_name: str

    def json(self):
        return {
            "user_id": str(self.user_id),
            "hotel_id": str(self.hotel_id),
            "price": str(self.price),
            "resident_name": str(self.resident_name)
        }


class CreateBookingRequest(BaseModel):
    user_id: UUID
    hotel_id: UUID
    price: str
    resident_name: str
