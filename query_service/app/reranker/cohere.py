import cohere
from app.config.settings import settings

co = cohere.ClientV2(
    api_key=settings.cohere_api_key
)


def rerank(question, chunks):
    return co.rerank(
        model="rerank-v3.5",
        query=question,
        documents=chunks,
        top_n=3,
    )