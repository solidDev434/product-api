from redis_om import get_redis_connection
from core.config import config

redis = get_redis_connection(
    port=config.REDIS_PORT,
    host=config.REDIS_HOST,
    password=config.REDIS_PASSWORD,
    decode_responses=True
)
