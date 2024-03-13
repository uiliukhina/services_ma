import uuid
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Body, Response

from app.models.hotel import Hotel, CreateHotelRequest
# from app.rabbitmq import send_booking
from app.services.hotel_catalog_service import HotelCatalogService

import prometheus_client

hotel_catalog_router = APIRouter(prefix='/hotel-catalog', tags=['HotelCatalog'])

metrics_router = APIRouter(tags=['Metrics'])

get_hotels_count = prometheus_client.Counter(
    "get_hotels_count",
    "Number of get requests for hotels"
)

get_hotel_count = prometheus_client.Counter(
    "get_hotel_count",
    "Number of get requests for hotel by id"
)

add_hotel_count = prometheus_client.Counter(
    "add_hotel_count",
    "Number of created hotels"
)
update_hotel_count = prometheus_client.Counter(
    "update_hotel_count",
    "Number of updated hotels"
)

delete_hotel_count = prometheus_client.Counter(
    "delete_hotel_count",
    "Number of deleted hotels"
)

failed_get_hotel_count = prometheus_client.Counter(
    "failed_get_hotel_count",
    "Number of failed attempts to get hotel by id"
)

name = 'HotelCatalog with Booking Service'


@hotel_catalog_router.get('/')
def get_hotels(hotel_catalog_service: HotelCatalogService = Depends(HotelCatalogService)) -> list[Hotel]:
    get_hotels_count.inc(1)
    return hotel_catalog_service.get_hotels()


# @hotel_catalog_router.get('/test')
# def get_hotels() -> str:
#     with tracer.start_as_current_span("server_request"):
#         return "it works!"


@hotel_catalog_router.get('/{hotel_id}')
def get_hotel(hotel_id: UUID, hotel_catalog_service: HotelCatalogService = Depends(HotelCatalogService)) -> Hotel:
    hotel = hotel_catalog_service.get_hotel_by_id(hotel_id)
    if hotel:
        get_hotels_count.inc(1)
        return hotel.dict()
    else:
        failed_get_hotel_count.inc(1)
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
    add_hotel_count.inc(1)
    return new_hotel.dict()


@hotel_catalog_router.put('/update/{hotel_id}')
def update_hotel(hotel_id: UUID, request: CreateHotelRequest,
                 hotel_catalog_service: HotelCatalogService = Depends(HotelCatalogService)) -> Hotel:
    updated_hotel = hotel_catalog_service.update_hotel(hotel_id, request.name, request.image_url, request.city,
                                                       request.description)

    update_hotel_count.inc(1)
    return updated_hotel.dict()


@hotel_catalog_router.delete('/delete/{hotel_id}')
def delete_hotel(hotel_id: UUID, hotel_catalog_service: HotelCatalogService = Depends(HotelCatalogService)) -> None:
    hotel_catalog_service.delete_hotel(hotel_id)
    delete_hotel_count.inc(1)
    return {'message': 'Hotel deleted successfully'}


@metrics_router.get('/metrics')
def get_metrics():
    return Response(
        media_type="text/plain",
        content=prometheus_client.generate_latest()
    )
