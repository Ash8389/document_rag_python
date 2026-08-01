
from app.qdrant.get_client import client
from app.models.chunk_schema import Chunk
from app.repo.vector_repo import VectorRepository


class QdrantRepository(VectorRepository):

    async def search(self, collection_name: str, embedding_vector: list[float], limit: int = 10) -> list[Chunk] :

        chunks = []

        points = client.query_points(
            collection_name=collection_name,
            query=embedding_vector,
            limit=limit,
        )
        for point in points.points:
            chunks.append(
                Chunk(
                    chunk_id = point.id,
                    content = point.payload["content"],
                    metadata= {
                        "source": point.payload["source"],
                        "page": point.payload["page"],
                        "chunk_idx": point.payload["chunk_idx"]
                        },
                    score = point.score
                )
            )
            
        return chunks