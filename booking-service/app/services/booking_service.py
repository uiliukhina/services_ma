from uuid import UUID

from fastapi import Depends
from pydantic import BaseModel, ConfigDict
from typing import List
from app.models.booking import Booking
from app.repositories.booking_repo import BookingRepo


class BookingService:
    booking_repo: BookingRepo

    def __init__(self, bkng_repo: BookingRepo = Depends(BookingRepo)) -> None:
        self.booking_repo = bkng_repo

    def get_bookings_for_user(self, user_id: UUID) -> List[Booking]:
        return self.booking_repo.get_bookings_for_user(user_id)

    def create_booking(self,
                       user_id: UUID,
                       hotel_id: UUID,
                       price: str,
                       resident_name) -> Booking:
        return self.booking_repo.create_booking(user_id=user_id,
                                                hotel_id=hotel_id,
                                                price=price,
                                                resident_name=resident_name)

    def remove_booking(self, booking_id: UUID) -> None:
        self.booking_repo.remove_booking(booking_id)
