import pathlib
from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.openapi.docs import get_redoc_html
from fastapi.staticfiles import StaticFiles
from prometheus_fastapi_instrumentator import Instrumentator

from deforestation_api.openapi import openapi
from deforestation_api.dependencies.deforestationdata import (
    fetch_deforestation_data,
    deforestation_data_fetcher,
)
from deforestation_api.routers import deforestation, healthcheck
from deforestation_api.settings import settings

import asyncio


@asynccontextmanager
async def lifespan(deforestation_app: FastAPI):
    await fetch_deforestation_data(deforestation_app)
    asyncio.create_task(deforestation_data_fetcher(deforestation_app))
    yield


app = FastAPI(
    lifespan=lifespan,
    root_path=settings.api_root_path,
    redoc_url=None,
)
app.include_router(deforestation.router)
app.include_router(healthcheck.router)

# The OpenEPI logo needs to be served as a static file since it is referenced in the OpenAPI schema
app.mount("/static", StaticFiles(directory="deforestation_api/assets/"), name="static")

logging.basicConfig(level=logging.INFO)

example_code_dir = pathlib.Path(__file__).parent / "example_code"
app.openapi_schema = openapi.custom_openapi(app, example_code_dir)
Instrumentator().instrument(app).expose(app)


@app.get("/redoc", include_in_schema=False)
def redoc():
    return get_redoc_html(
        openapi_url=f"{settings.api_root_path}/openapi.json",
        title="Deforestation API",
        redoc_favicon_url="https://www.openepi.io/favicon.ico",
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "deforestation_api.__main__:app",
        host=settings.uvicorn_host,
        port=settings.uvicorn_port,
        reload=settings.uvicorn_reload,
        proxy_headers=settings.uvicorn_proxy_headers,
    )
