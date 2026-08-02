from fastapi import Depends

from app.repo.qdrant_repo import QdrantRepository
from app.services.chat_service import ChatService
from app.redis.redis import RedisClient
from app.chat.openai_chat_model import OpenAiChatModel

def get_qdrant_repo():
    return QdrantRepository()

def get_redis_client():
    return RedisClient()

def get_open_ai_chat_model():
    return OpenAiChatModel()


def get_chat_service(
        qdrant : QdrantRepository = Depends(get_qdrant_repo),
        redis_client : RedisClient = Depends(get_redis_client),
        chat_model: OpenAiChatModel = Depends(get_open_ai_chat_model)
):
    return ChatService(qdrant, redis_client, chat_model)