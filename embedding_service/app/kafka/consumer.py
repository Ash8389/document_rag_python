import json, asyncio

from app.kafka import get_kafka_consumer
# from app.qdrant.insert_chunks import insert_chunks
from app.services.embedding_service import embedding_service


async def consume_chunks():

    chunks = []

    async for msg in get_kafka_consumer.consumer:
        event = json.loads(msg.value)

        if event["content"]=="END" :
            await embedding_service(chunks)
            chunks.clear()

        chunks.append(event)
        if len(chunks) >= 10 :
            await embedding_service(chunks)
            chunks.clear()