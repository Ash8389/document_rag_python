import json

from app.kafka.config import producer

async def produce(chunks):
    
    for chunk in chunks:
        message = {
            "chunk_id" : chunk.metadata["chunk_id"],
            "content": chunk.page_content,
            "metadata": chunk.metadata
        }

        await producer.send_and_wait(
            "document.chunks",
            json.dumps(message).encode()
        )

    await producer.send(
            "document.chunks",
             json.dumps({"content": "END"}).encode()
        )