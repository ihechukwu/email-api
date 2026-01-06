import uuid
from redis.asyncio import Redis
from app.core.config import settings
from fastapi import HTTPException, status

redis = Redis.from_url(settings.REDIS_URL, decode_responses=True)

RATE_LIMIT = 100
WINDOW_SECONDS = 60


async def check_rate_limit(api_key_id: uuid.UUID):
    key = f"rate_limit:{api_key_id}"

    count = await redis.incr(key)
    if count == 0:
        await redis.expire(key, WINDOW_SECONDS)

    if count > RATE_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded, try again later",
        )
