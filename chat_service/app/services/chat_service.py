from app.repo.qdrant_repo import QdrantRepository
from app.models.llm_response import LlmResponse
from app.config.settings import settings
from app.processors.embed import embed_text
from app.chat.openai_chat_model import chat


class ChatService:
    def __init__(self, repo: QdrantRepository):
        self.repo = repo
        self.collection_name = settings.qdrant_collection

    async def chat_service(self, question):
        embedding_vector = await embed_text(question)
        chunks = await self.repo.search(self.collection_name, embedding_vector)
        context = []

        for chunk in chunks :
            context.append(chunk.content)

        result = chat(question=question, context=context)
        return LlmResponse(
            answer=result.content,
            model_name=result.response_metadata["model_name"],
            input_tokens=result.usage_metadata["input_tokens"],
            output_tokens=result.usage_metadata["output_tokens"],
            total_tokens=result.usage_metadata["total_tokens"]
        )

