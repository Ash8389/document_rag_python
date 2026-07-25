import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.qdrant.get_client import client
from app.kafka.get_kafka_consumer import get_kafka_consumer, stop_consumer
from app.qdrant.create_collection import create_collection
from app.kafka.consumer import consume_chunks

@asynccontextmanager
async def lifespan(app):
    create_collection(client)
    await get_kafka_consumer()

    consumer_task = asyncio.create_task(consume_chunks())

    yield

    consumer_task.cancel()
    await stop_consumer()

app = FastAPI(
    title="Embedding Service",
    description="This service is used for Embedding chunks in Qdrant DB.",
    version="1.0",
    lifespan=lifespan
)
