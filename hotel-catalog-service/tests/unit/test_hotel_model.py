import pytest
from uuid import uuid4
from pydantic import ValidationError

from app.models.hotel import Hotel, CreateHotelRequest


def test_hotel_creation():
    id = uuid4()
    name = 'Ilukhina First Hotel'
    image_url = 'https://ilukhina-hotel.com'
    city = 'Moscow'
    description = 'Hotel Description'

    hotel = Hotel(id=id, name=name, image_url=image_url, city=city,
                  description=description)

    assert dict(hotel) == {'id': id, 'name': name, 'image_url': image_url,
                           'city': city, 'description': description}


def test_hotel_name_required():
    id = uuid4()
    name = 'Ilukhina Second Hotel'
    image_url = 'https://ilukhina-hotel.com'
    city = 'Moscow'
    description = 'Hotel Description'

    with pytest.raises(ValidationError):
        Hotel(id=id, image_url=image_url, city=city,
              description=description)


def test_hotel_city_required():
    id = uuid4()
    name = 'Ilukhina First Hotel'
    image_url = 'https://ilukhina-hotel.com'
    city = 'Moscow'
    description = 'Hotel Description'

    with pytest.raises(ValidationError):
        Hotel(id=id, name=name, image_url=image_url,
              description=description)


def test_image_url_required():
    id = uuid4()
    name = 'Ilukhina First Hotel'
    image_url = 'https://ilukhina-hotel.com'
    city = 'Moscow'
    description = 'Hotel Description'

    with pytest.raises(ValidationError):
        Hotel(id=id, name=name, city=city,
              description=description)
