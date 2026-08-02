from app.repo.qdrant_repo import QdrantRepository
from app.models.llm_response import LlmResponse
from app.reranker.cohere import rerank
from app.config.settings import settings
from app.processors.embed import embed_text
from app.chat.openai_chat_model import OpenAiChatModel
from app.redis.redis import RedisClient


class ChatService:
    def __init__(self, repo: QdrantRepository, redis_client: RedisClient, chat_model: OpenAiChatModel):
        self.repo = repo
        self.collection_name = settings.qdrant_collection
        self.redis_client = redis_client
        self.chat_model = chat_model


    async def chat_service(self, question):

        # await self.redis_client.delete(question)

        cache_res = await self.redis_client.get(question) 

        if cache_res:
            return LlmResponse.model_validate_json(cache_res)


        embedding_vector = await embed_text(question)
        chunks = await self.repo.search(self.collection_name, embedding_vector)

        contents = [chunk.content for chunk in chunks]
        # print(len(chunks))
        
        reranked = rerank(question=question, chunks=contents)
        # print(reranked)

        context = []

        for res in reranked.results:
            context.append(chunks[res.index].content)

        result = self.chat_model.chat(question=question, context=context)

        llmResponse = LlmResponse(
            answer=result.content,
            model_name=result.response_metadata["model_name"],
            input_tokens=result.usage_metadata["input_tokens"],
            output_tokens=result.usage_metadata["output_tokens"],
            total_tokens=result.usage_metadata["total_tokens"]
        )

        await self.redis_client.set(
            question,
            llmResponse.model_dump_json()
        )

        return llmResponse