import pytest
from uuid import uuid4
from time import sleep
from datetime import datetime

from app.models.hotel import Hotel
from app.repositories.bd_hotel_repo import HotelRepo

sleep(5)


@pytest.fixture()
def hotel_repo() -> HotelRepo:
    repo = HotelRepo()
    return repo


@pytest.fixture(scope='session')
def first_hotel() -> Hotel:
    id = uuid4()
    name = 'Ilukhina First Hotel'
    image_url = 'https://ilukhina-hotel.com'
    city = 'Moscow'
    description = 'Hotel Description'

    return Hotel(id=id, name=name, image_url=image_url, city=city,
                 description=description)


@pytest.fixture(scope='session')
def second_hotel() -> Hotel:
    id = uuid4()
    name = 'Ilukhina Second Hotel'
    image_url = 'https://ilukhina-second-hotel.com'
    city = 'Sochi'
    description = 'Second Hotel Description'

    return Hotel(id=id, name=name, image_url=image_url, city=city,
                 description=description)


def test_add_first_hotel(first_hotel: Hotel, hotel_repo: HotelRepo) -> None:
    assert hotel_repo.add_hotel(first_hotel) == first_hotel


def test_get_hotel_by_id(hotel_repo: HotelRepo) -> None:
    hotel = hotel_repo.get_hotels()[0]
    hotel_by_id = hotel_repo.get_hotel_by_id(hotel.id)
    assert hotel.id == hotel_by_id.id


def test_get_hotel_by_id_error(hotel_repo: HotelRepo) -> None:
    with pytest.raises(KeyError):
        hotel_repo.get_hotel_by_id(uuid4())


def test_add_second_hotel( second_hotel: Hotel, hotel_repo: HotelRepo) -> None:
    assert hotel_repo.add_hotel(second_hotel) == second_hotel
    hotels = hotel_repo.get_hotels()
    assert hotels[-1] == second_hotel
