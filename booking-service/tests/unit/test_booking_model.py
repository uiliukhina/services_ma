import pytest
from uuid import uuid4
from pydantic import ValidationError

from app.models.booking import Booking


def test_booking_creation():
    id = uuid4()
    user_id = uuid4()
    hotel_id = uuid4()
    price = "1000"
    resident_name = "Ilukhina"

    booking = Booking(id=id, user_id=user_id, hotel_id=hotel_id, price=price, resident_name=resident_name)

    assert booking.id == id
    assert booking.user_id == user_id
    assert booking.hotel_id == hotel_id


def test_booking_user_id_required():
    id = uuid4()
    hotel_id = uuid4()
    price = "1000"
    resident_name = "Ilukhina"

    with pytest.raises(ValidationError):
        Booking(id=id, hotel_id=hotel_id, price=price, resident_name=resident_name)


def test_booking_hotel_id_required():
    id = uuid4()
    user_id = uuid4()
    price = "1000"
    resident_name = "Ilukhina"

    with pytest.raises(ValidationError):
        Booking(id=id, user_id=user_id, price=price, resident_name=resident_name)
