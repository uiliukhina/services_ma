import uuid
from uuid import UUID
from typing import List

from app.models.booking import Booking


class BookingRepo:
    bookings: List[Booking] = []

    def get_bookings_for_user(self, user_id: UUID) -> List[Booking]:
        return [bkng for bkng in self.bookings if bkng.user_id == user_id]

    def create_booking(self,
                       user_id: UUID,
                       hotel_id: UUID,
                       price: str,
                       resident_name: str
                       ) -> Booking:
        booking = Booking(id=uuid.uuid4(),
                          user_id=user_id,
                          hotel_id=hotel_id,
                          price=price,
                          resident_name=resident_name)
        self.bookings.append(booking)
        return booking

    def remove_booking(self, booking_id: UUID) -> None:
        before_del = self.bookings
        self.bookings = [bkng for bkng in self.bookings if bkng.id != booking_id]

        if len(before_del) == len(self.bookings):
            raise ValueError
