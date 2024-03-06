import uuid
from uuid import UUID

from fastapi import Depends
from pydantic import BaseModel, ConfigDict
from typing import List
from app.models.hotel import Hotel
from app.repositories.bd_hotel_repo import HotelRepo


class HotelCatalogService:
    hotel_repo: HotelRepo

    def __init__(self, hotel_repo: HotelRepo = Depends(HotelRepo)) -> None:
        self.hotel_repo = hotel_repo

    def get_hotels(self) -> List[Hotel]:
        return self.hotel_repo.get_hotels()

    def get_hotel_by_id(self, hotel_id: UUID) -> Hotel:
        return self.hotel_repo.get_hotel_by_id(hotel_id)

    def add_hotel(self, name: str, image_url: str, city: str, description: str) -> Hotel:
        new_hotel = Hotel(id=uuid.uuid4(), name=name, image_url=image_url, city=city, description=description)
        return self.hotel_repo.add_hotel(new_hotel)

    def update_hotel(self, hotel_id: UUID, name: str, image_url: str, city: str, description: str) -> Hotel:
        hotel = self.hotel_repo.get_hotel_by_id(hotel_id)
        hotel.name = name
        hotel.image_url = image_url
        hotel.city = city
        hotel.description = description
        return self.hotel_repo.update_hotel(hotel)

    def delete_hotel(self, hotel_id: UUID) -> None:
        self.hotel_repo.delete_hotel(hotel_id)
