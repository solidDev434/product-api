from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi_cache import caches, close_caches
from redis_om import Migrator
from fastapi_cache.backends.redis import RedisCacheBackend, CACHE_KEY

from contextlib import asynccontextmanager


from schema import Product
from core.config import config


@asynccontextmanager
async def lifespan(app: FastAPI):
    Migrator().run()

    rc = RedisCacheBackend(
        f"redis://{config.REDIS_USER}:{config.REDIS_PASSWORD}@{config.REDIS_HOST}:{config.REDIS_PORT}")
    caches.set(CACHE_KEY, rc)

    yield
    await close_caches()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/products")
async def root():
    return Product.find().all()


@app.post("/products")
async def create(product: Product):
    return product.save()


@app.delete("/products/{product_id}")
async def create(product_id: str):
    Product.delete(pk=product_id)
    return {"message": f"Product {product_id} deleted successgfully"}
