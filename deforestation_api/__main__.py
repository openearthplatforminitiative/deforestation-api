from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from deforestation_api.settings import Settings
from deforestation_api.routers import deforestation, healthcheck


@asynccontextmanager
async def lifespan(_: FastAPI):
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")
    yield


settings = Settings()
app = FastAPI(title="deforestation API", version=settings.version, lifespan=lifespan)
app.include_router(deforestation.router)
app.include_router(healthcheck.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "deforestation_api.__main__:app",
        host=settings.uvicorn_host,
        port=settings.uvicorn_port,
        reload=settings.uvicorn_reload,
        proxy_headers=settings.uvicorn_proxy_headers,
    )
