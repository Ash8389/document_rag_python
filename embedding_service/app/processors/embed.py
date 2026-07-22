import asyncio

from langchain_openai import OpenAIEmbeddings
from app.config.settings import settings

embedding_model = OpenAIEmbeddings(
    base_url=settings.jina_base_url,
    api_key=settings.jina_api_key,
    model=settings.jina_model,
    dimensions=settings.embedding_dimension,
    check_embedding_ctx_length=False
)

async def embed_text(contents):
    embedding = await embedding_model.aembed_documents(contents)
    print(contents[0])
    print("-"*20)

    return embedding