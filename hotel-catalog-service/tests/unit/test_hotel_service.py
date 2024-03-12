import pytest
from uuid import uuid4, UUID

from app.services.hotel_catalog_service import HotelCatalogService
from app.repositories.hotel_repo import HotelRepo
from app.models.hotel import Hotel


@pytest.fixture(scope='session')
def hotel_service() -> HotelCatalogService:
    return HotelCatalogService(HotelRepo(clear=True))


@pytest.fixture()
def hotel_repo() -> HotelRepo:
    return HotelRepo()


@pytest.fixture(scope='session')
def first_hotel_data() -> tuple[UUID, str, str, str, str]:
    return uuid4(), 'hotel1', 'image_url1', 'city1', 'desc1'


@pytest.fixture(scope='session')
def second_hotel_data() -> tuple[UUID, str, str, str, str]:
    return uuid4(), 'hotel2', 'image_url2', 'city2', 'desc2'


def test_empty_hotels(hotel_service: HotelCatalogService) -> None:
    assert hotel_service.get_hotels() == []


def test_add_hotel(
        first_hotel_data,
        hotel_service: HotelCatalogService
) -> None:
    id, name, image_url, city, description = first_hotel_data
    hotel_service.add_hotel(name, image_url, city, description)
    hotel = hotel_service.get_hotels()[0]
    assert hotel.name == name
    assert hotel.image_url == image_url
    assert hotel.city == city
    assert hotel.description == description


def test_add_second_hotel(
        second_hotel_data,
        hotel_service: HotelCatalogService
) -> None:
    id, name, image_url, city, description = second_hotel_data
    hotel_service.add_hotel(name, image_url, city, description)
    hotel = hotel_service.get_hotels()[1]
    assert hotel.name == name
    assert hotel.image_url == image_url
    assert hotel.city == city
    assert hotel.description == description


def test_get_hotels_full(
        first_hotel_data,
        second_hotel_data,
        hotel_service: HotelCatalogService
) -> None:
    hotels = hotel_service.get_hotels()
    assert len(hotels) == 2
    assert hotels[0].name == first_hotel_data[1]
    assert hotels[1].name == second_hotel_data[1]


def test_get_hotels(hotel_service: HotelCatalogService,
                   first_hotel_data: tuple[UUID, str, str, str, str],
                   second_hotel_data: tuple[UUID, str, str, str, str]) -> None:
    hotels = hotel_service.get_hotels()

    # Check that the list of hotels is not empty and contains the expected hotels
    assert hotels
    assert len(hotels) == 2

    _, name1, image_url1, city1, desc1 = first_hotel_data
    _, name2, image_url2, city2, desc2 = second_hotel_data

    hotel_service.add_hotel(name1, image_url1, city1, desc1)
    hotel_service.add_hotel(name2, image_url2, city2, desc2)

    hotels_after_addition = hotel_service.get_hotels()
    assert len(hotels_after_addition) == 4

    # Check that the data of the hotels matches the expected data

    assert hotels_after_addition[2].name == first_hotel_data[1]
    assert hotels_after_addition[2].image_url == first_hotel_data[2]
    assert hotels_after_addition[2].city == first_hotel_data[3]
    assert hotels_after_addition[2].description == first_hotel_data[4]

    assert hotels_after_addition[3].name == second_hotel_data[1]
    assert hotels_after_addition[3].image_url == second_hotel_data[2]
    assert hotels_after_addition[3].city == second_hotel_data[3]
    assert hotels_after_addition[3].description == second_hotel_data[4]


def test_get_hotel_by_id(hotel_service: HotelCatalogService,
                        first_hotel_data: tuple[UUID, str, str, str, str]) -> None:

    hotel = hotel_service.get_hotels()[0]
    first_hotel_id = hotel.id

    hotel = hotel_service.get_hotel_by_id(first_hotel_id)

    assert hotel.name == first_hotel_data[1]
    assert hotel.image_url == first_hotel_data[2]
    assert hotel.city == first_hotel_data[3]
    assert hotel.description == first_hotel_data[4]
