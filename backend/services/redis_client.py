import redis.asyncio as redis
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

class RedisClient:
    def __init__(self):
        self.redis = None

    async def connect(self):
        if not self.redis:
            self.redis = redis.from_url(REDIS_URL, decode_responses=True)

    async def close(self):
        if self.redis:
            await self.redis.close()
            self.redis = None

    async def get(self, key):
        return await self.redis.get(key)

    async def set(self, key, value, ex=None):
        await self.redis.set(key, value, ex=ex)

    async def delete(self, key):
        await self.redis.delete(key)

    async def exists(self, key):
        return await self.redis.exists(key)

    async def hset(self, key, mapping):
        await self.redis.hset(key, mapping=mapping)

    async def hgetall(self, key):
        return await self.redis.hgetall(key)

    async def lpush(self, key, value):
        await self.redis.lpush(key, value)

    async def lrange(self, key, start, stop):
        return await self.redis.lrange(key, start, stop)

redis_client = RedisClient()
