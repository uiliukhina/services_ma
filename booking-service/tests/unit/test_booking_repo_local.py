import pytest
from uuid import uuid4
from app.models.booking import Booking
from app.repositories.booking_repo import BookingRepo


@pytest.fixture(scope='session')
def booking_repo() -> BookingRepo:
    return BookingRepo()


@pytest.fixture(scope='session')
def first_booking() -> Booking:
    id = uuid4()
    user_id = uuid4()
    hotel_id = uuid4()
    price = "1000"
    resident_name = "First Ilukhina"

    return Booking(id=id, user_id=user_id, hotel_id=hotel_id, price=price, resident_name=resident_name)


@pytest.fixture(scope='session')
def second_booking() -> Booking:
    id = uuid4()
    user_id = uuid4()
    hotel_id = uuid4()
    price = "2000"
    resident_name = "Second Ilukhina"

    return Booking(id=id, user_id=user_id, hotel_id=hotel_id, price=price, resident_name=resident_name)


booking_test_repo = BookingRepo()


def test_empty_booking_list() -> None:
    assert booking_test_repo.get_bookings_for_user(uuid4()) == []


def test_create_booking(booking_repo: BookingRepo,
                        first_booking: Booking) -> None:
    booking_repo.create_booking(
        first_booking.user_id,
        first_booking.hotel_id,
        first_booking.price,
        first_booking.resident_name
    )
    bookings = booking_repo.get_bookings_for_user(first_booking.user_id)
    assert len(bookings) == 1
    assert bookings[0].hotel_id == first_booking.hotel_id


def test_remove_booking(booking_repo: BookingRepo,
                        first_booking: Booking) -> None:
    booking = booking_repo.get_bookings_for_user(first_booking.user_id)[0]
    booking_repo.remove_booking(booking.id)
    bookings = booking_repo.get_bookings_for_user(first_booking.user_id)
    assert len(bookings) == 0


def test_remove_nonexistent_booking(booking_repo: BookingRepo) -> None:
    with pytest.raises(ValueError):
        booking_repo.remove_booking(uuid4())
