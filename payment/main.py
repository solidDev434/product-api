from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi_cache import caches, close_caches
from redis_om import Migrator
from fastapi_cache.backends.redis import RedisCacheBackend, CACHE_KEY

from contextlib import asynccontextmanager

from core.config import config


@asynccontextmanager
async def lifespan(app: FastAPI):
    Migrator().run()

    rc = RedisCacheBackend(config.REDIS_URI)
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
