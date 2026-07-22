from qdrant_client import QdrantClient
from app.config.settings import settings


client = QdrantClient(
    host=settings.qdrant_host,
    port=settings.qdrant_port
)
