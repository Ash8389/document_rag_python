import redis.asyncio as redis
from app.config.settings import settings

class RedisClient:
    def __init__(self):
        self.client = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            decode_responses=True
        )

    async def delete(self, question):
        await self.client.delete(question)

    async def set(self, question, answer):
        await self.client.set(question, answer, ex=settings.redis_ttl_min)

    async def get(self, question):
        res = await self.client.get(question)
        return res