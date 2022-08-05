import json

import aio_pika
import aio_pika.abc

from app.aws.dynamodb import add_innotter_data_to_db
from app.config import settings


async def consume(loop):
    connection = await aio_pika.connect_robust(
        f"amqp://{settings.RABBITMQ_DEFAULT_USER}:{settings.RABBITMQ_DEFAULT_PASS}@{settings.RABBITMQ_HOSTNAME}/",
        loop=loop
    )

    async with connection:
        queue_name = "stats"

        channel: aio_pika.abc.AbstractChannel = await connection.channel()

        queue: aio_pika.abc.AbstractQueue = await channel.declare_queue(
            queue_name,
            durable=True
        )

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    data = json.loads(message.body)

                    await add_innotter_data_to_db(id=data.get('id'), data=data)

                    if queue.name in message.body.decode():
                        break
