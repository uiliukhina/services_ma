# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import asyncio
import asyncio
from fastapi import FastAPI
from logging_loki import LokiHandler
import logging


from app.settings import settings

from app.endpoints.hotel_catalog_router import hotel_catalog_router, metrics_router

name = 'HotelCatalog with Bookings Service'

app = FastAPI(title=name)

loki_logs_handler = LokiHandler(
    url="http://loki:3100/loki/api/v1/push",
    tags={"application": "fastapi"},
    version="1",
)

logger = logging.getLogger("uvicorn.access")
logger.addHandler(loki_logs_handler)

app.include_router(hotel_catalog_router, prefix='/hotel-api')
app.include_router(metrics_router)
