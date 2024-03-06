import uuid
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Body

from app.models.hotel import Hotel, CreateHotelRequest
# from app.rabbitmq import send_booking
from app.services.hotel_catalog_service import HotelCatalogService

hotel_catalog_router = APIRouter(prefix='/hotel-catalog', tags=['HotelCatalog'])

name = 'HotelCatalog with Booking Service'


@hotel_catalog_router.get('/')
def get_hotels(hotel_catalog_service: HotelCatalogService = Depends(HotelCatalogService)) -> list[Hotel]:
    return hotel_catalog_service.get_hotels()


# @hotel_catalog_router.get('/test')
# def get_hotels() -> str:
#     with tracer.start_as_current_span("server_request"):
#         return "it works!"


@hotel_catalog_router.get('/{hotel_id}')
def get_hotel(hotel_id: UUID, hotel_catalog_service: HotelCatalogService = Depends(HotelCatalogService)) -> Hotel:
    hotel = hotel_catalog_service.get_hotel_by_id(hotel_id)
    if hotel:
        return hotel.dict()
    else:
        raise HTTPException(404, f'Hotelwith id={hotel_id} not found')


@hotel_catalog_router.post('/add')
def add_hotel(request: CreateHotelRequest,
              hotel_catalog_service: HotelCatalogService = Depends(HotelCatalogService)) -> Hotel:
    new_hotel = hotel_catalog_service.add_hotel(
        name=request.name,
        city=request.city,
        image_url=request.image_url,
        description=request.description)

    user_id = uuid.uuid4()

    # await send_booking(user_id, new_hotel.id)

    return new_hotel.dict()


@hotel_catalog_router.put('/update/{hotel_id}')
def update_hotel(hotel_id: UUID, request: CreateHotelRequest,
                 hotel_catalog_service: HotelCatalogService = Depends(HotelCatalogService)) -> Hotel:
    updated_hotel = hotel_catalog_service.update_hotel(hotel_id, request.name, request.image_url, request.city,
                                                       request.description)
    return updated_hotel.dict()


@hotel_catalog_router.delete('/delete/{hotel_id}')
def delete_hotel(hotel_id: UUID, hotel_catalog_service: HotelCatalogService = Depends(HotelCatalogService)) -> None:
    hotel_catalog_service.delete_hotel(hotel_id)
    return {'message': 'Hotel deleted successfully'}
