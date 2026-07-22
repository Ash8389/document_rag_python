from abc import ABC, abstractmethod

from app.models.chunk_schema import Chunk

class VectorRepository(ABC) :

    @abstractmethod
    async def search(
        self,
        collection_name: str,
        vector: list[float],
        limit: int = 5
    ) -> list[Chunk]:
        pass