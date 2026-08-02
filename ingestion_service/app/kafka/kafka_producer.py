import json

from app.kafka import config

async def produce(chunks):
    
    for chunk in chunks:
        message = {
            "chunk_id" : chunk.metadata["chunk_id"],
            "content": chunk.page_content,
            "metadata": chunk.metadata
        }

        await config.producer.send_and_wait(
            "document.chunks",
            json.dumps(message).encode()
        )

    await config.producer.send(
            "document.chunks",
             json.dumps({"content": "END"}).encode()
        )