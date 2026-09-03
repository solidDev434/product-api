from redis_om import HashModel
from core.redis import redis


class Product(HashModel, index=True):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis
