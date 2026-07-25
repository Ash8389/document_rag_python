from fastapi import Depends

from app.repo.qdrant_repo import QdrantRepository
from app.services.chat_service import ChatService

def get_qdrant_repo():
    return QdrantRepository()


def get_chat_service(qdrant : QdrantRepository = Depends(get_qdrant_repo)):
    return ChatService(qdrant)