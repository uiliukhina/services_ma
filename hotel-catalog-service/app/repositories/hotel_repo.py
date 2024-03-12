from uuid import UUID, uuid4
from typing import List
from app.models.hotel import Hotel


class HotelRepo:
    hotels = [
        Hotel(id=uuid4(), name='Hotel', image_url="https", city="Moscow", description='HotelDescription')
    ]

    def __init__(self, clear: bool = False) -> None:

        if clear:
            self.hotels = []

    def get_hotels(self) -> List[Hotel]:
        return self.hotels

    def get_hotel_by_id(self, hotel_id: UUID) -> Hotel:
        hotel = next((hotel for hotel in self.hotels if hotel.id == hotel_id), None)

        if hotel is not None:
            return hotel
        else:
            raise KeyError

    def add_hotel(self, hotel: Hotel) -> Hotel:
        self.hotels.append(hotel)
        return hotel

    def delete_hotel(self, hotel_id: UUID) -> None:
        self.hotels = [hotel for hotel in self.hotels if hotel.id != hotel_id]
