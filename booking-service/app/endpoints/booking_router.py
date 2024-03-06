from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Body
from app.services.booking_service import BookingService
from app.models.booking import Booking, CreateBookingRequest

booking_router = APIRouter(prefix='/bookings', tags=['Bookings'])


@booking_router.get('/user/{user_id}')
def get_bookings_for_user(user_id: UUID,
                                 booking_service: BookingService = Depends(BookingService)) -> \
        list[Booking]:
    return booking_service.get_bookings_for_user(user_id)


@booking_router.post('/add')
def add_booking(request: CreateBookingRequest, booking_service: BookingService = Depends(
    BookingService)) -> Booking:
    new_booking = booking_service.create_booking(request.user_id,
                                                 request.hotel_id,
                                                 request.price,
                                                 request.resident_name,
                                                 )
    return new_booking.dict()


@booking_router.delete('/remove/{booking_id}')
def remove_booking(booking_id: UUID,
                          booking_service: BookingService = Depends(BookingService)) -> None:
    booking_service.remove_booking(booking_id)
    return {'message': 'Booking removed successfully'}
