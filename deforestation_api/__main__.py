from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI

from deforestation_api.dependencies.deforestationdata import fetch_deforestation_data, deforestation_data_fetcher
from deforestation_api.routers import deforestation, healthcheck
from deforestation_api.settings import settings

import asyncio

@asynccontextmanager
async def lifespan(deforestation_app: FastAPI):
    await fetch_deforestation_data(deforestation_app)
    asyncio.create_task(deforestation_data_fetcher(deforestation_app))
    yield


app = FastAPI(
    title="Deforestation API",
    lifespan=lifespan,
    version=settings.version,
    root_path=settings.api_root_path,
)
app.include_router(deforestation.router)
app.include_router(healthcheck.router)

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "deforestation_api.__main__:app",
        host=settings.uvicorn_host,
        port=settings.uvicorn_port,
        reload=settings.uvicorn_reload,
        proxy_headers=settings.uvicorn_proxy_headers,
    )
