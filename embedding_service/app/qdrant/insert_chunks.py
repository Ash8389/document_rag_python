from qdrant_client.models import PointStruct

from app.qdrant.get_client import client
from app.config.settings import settings

def insert_chunks(embeddings, chunks):
    points = []

    for chunk, embedding in zip(chunks, embeddings):
        payload = {
            "content" : chunk["content"],
            "source" : chunk["metadata"]["source"],
            "page" : chunk["metadata"]["page"],
            "chunk_idx" : chunk["metadata"]["chunk_idx"],
        }
        points.append(
            PointStruct(
                id = chunk["chunk_id"],
                vector = embedding,
                payload = payload
            )
        )

    client.upsert(
        collection_name=settings.qdrant_collection,
        points=points
    )