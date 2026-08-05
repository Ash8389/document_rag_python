from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.dependencies.dependencies import get_chat_service
from app.services.chat_service import ChatService
from app.models.llm_response import LlmResponse


class ChatRequest(BaseModel):
    question: str


router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)


@router.post("")
async def chat_post(body: ChatRequest, service: ChatService = Depends(get_chat_service)) -> LlmResponse:
    return await service.chat_service(question=body.question)


@router.get("")
async def chat_get(question: str, service: ChatService = Depends(get_chat_service)) -> LlmResponse:
    return await service.chat_service(question=question)
