import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.qdrant.get_client import client
from app.kafka.get_kafka_consumer import consumer
from app.qdrant.create_collection import create_collection
from app.kafka.consumer import consume_chunks


@asynccontextmanager
async def lifespan(app):
    create_collection(client)
    await consumer.start()

    consumer_task = asyncio.create_task(consume_chunks())

    yield

    consumer_task.cancel()
    await consumer.stop()

app = FastAPI(
    title="Embedding Service",
    description="This service is used for Embedding chunks in Qdrant DB.",
    version="1.0",
    lifespan=lifespan
)
