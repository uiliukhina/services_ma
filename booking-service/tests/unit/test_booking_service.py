import pytest
from uuid import uuid4, UUID
from app.models.booking import Booking
from app.services.booking_service import BookingService
from app.repositories.booking_repo import BookingRepo


@pytest.fixture(scope='session')
def booking_service() -> BookingService:
    return BookingService(BookingRepo())


@pytest.fixture(scope='session')
def first_booking_data() -> tuple[UUID, UUID, str, str]:
    return uuid4(), uuid4(), '435', "Ilukhina First"


@pytest.fixture(scope='session')
def second_booking_data() -> tuple[UUID, UUID, str, str]:
    return uuid4(), uuid4(), '23256', "Ilukhina Second"


def test_empty_bookings(booking_service: BookingService) -> None:
    assert booking_service.get_bookings_for_user(uuid4()) == []


def test_create_booking(
    booking_service: BookingService,
    first_booking_data: tuple[UUID, UUID, str, str]
) -> None:
    user_id, hotel_id, price, resident_name = first_booking_data
    booking = booking_service.create_booking(user_id, hotel_id, price, resident_name)
    bookings = booking_service.get_bookings_for_user(user_id)
    assert len(bookings) == 1
    assert bookings[0] == booking


def test_remove_booking(
    booking_service: BookingService,
    first_booking_data: tuple[UUID, UUID, str, str]
) -> None:
    user_id, _, _, _ = first_booking_data
    bkng = booking_service.get_bookings_for_user(user_id)[0]

    booking_service.remove_booking(bkng.id)
    bookings = booking_service.get_bookings_for_user(user_id)
    assert len(bookings) == 0


def test_remove_nonexistent_booking(
    booking_service: BookingService
) -> None:
    with pytest.raises(ValueError):
        booking_service.remove_booking(uuid4())
