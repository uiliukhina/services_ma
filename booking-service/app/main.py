# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import asyncio
from fastapi import FastAPI

from app import rabbitmq
from app.settings import settings

from app.endpoints.booking_router import booking_router

name = 'Hotels with Booking Service'

app = FastAPI(title=name)


# @app.on_event('startup')
# def startup():
#     print("ON STARTUP")
#     loop = asyncio.get_event_loop()
#     asyncio.ensure_future(rabbitmq.consume(loop))
#     print("ON STARTUP")


app.include_router(booking_router, prefix='/bkng-api')
