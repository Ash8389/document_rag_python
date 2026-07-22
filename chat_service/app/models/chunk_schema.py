from pydantic import BaseModel

class Chunk(BaseModel) :
    chunk_id: str
    content : str
    metadata: dict
    score: float