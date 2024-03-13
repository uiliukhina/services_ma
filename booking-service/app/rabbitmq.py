import json
import random
import traceback
import uuid
from asyncio import AbstractEventLoop
from uuid import UUID

from aio_pika import connect_robust, IncomingMessage, Message
from aio_pika.abc import AbstractRobustConnection
from aio_pika import connect_robust, IncomingMessage

from app.models.booking import Booking
from app.settings import settings


async def process_new_booking(msg: IncomingMessage):
    try:
        print("PROCESSING NEW RECOMMENDATION................")
        data = json.loads(msg.body.decode())
        print(data)
        bkng = Booking(**data)
        await save_booking(bkng)
    except Exception as e:
        traceback.print_exc()


async def save_booking(bkng: Booking):
    # Here you would implement your logic to save the booking
    # For demonstration, let's just print it
    print(f"Saving booking: {bkng}")


async def consume(loop: AbstractEventLoop) -> AbstractRobustConnection:
    connection = await connect_robust(settings.amqp_url, loop=loop)
    channel = await connection.channel()

    print("Consuming...")

    new_hotel_queue = await channel.declare_queue('ilukhina_update_queue', durable=True)

    await new_hotel_queue.consume(process_new_booking)

    print('Started RabbitMQ consuming for the library...')
    return connection
