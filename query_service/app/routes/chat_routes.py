from fastapi import APIRouter, Depends
from app.dependencies.dependencies import get_chat_service
from app.services.chat_service import ChatService
from app.models.llm_response import LlmResponse


router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

@router.get("")
async def chat(question, service : ChatService = Depends(get_chat_service)) -> LlmResponse :
    return await service.chat_service(question=question)