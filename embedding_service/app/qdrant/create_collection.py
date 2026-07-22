from qdrant_client.models import Distance
from qdrant_client.models import VectorParams
from qdrant_client import QdrantClient

from app.config.settings import settings


def create_collection(client: QdrantClient):
    collections = client.get_collections()

    names = [c.name for c in collections.collections]

    if settings.qdrant_collection not in names:
        client.create_collection(
            collection_name=settings.qdrant_collection,

            vectors_config=VectorParams(
                size=settings.embedding_dimension,
                distance=Distance.COSINE
            )
        )