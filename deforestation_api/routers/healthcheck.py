from fastapi import APIRouter
from fastapi import Response
from healthcheck import HealthCheck
from deforestation_api.settings import settings
import s3fs


router = APIRouter(tags=["health"])


def basin_data_available():
    s3 = s3fs.S3FileSystem(anon=True)
    if s3.exists(settings.basin_data_path):
        return True, "Basin data available"
    else:
        return False, "Basin data not available"


def lossyear_data_available():
    s3 = s3fs.S3FileSystem(anon=True)
    if s3.exists(settings.lossyear_data_path):
        return True, "Lossyear data available"
    else:
        return False, "Lossyear data not available"


health = HealthCheck()
health.add_section("version", settings.version)
health.add_check(basin_data_available)
health.add_check(lossyear_data_available)


@router.get(
    "/ready",
    summary="Check if this service is ready to receive requests",
    description="Returns a message describing the status of this service",
    tags=["health"],
)
async def ready() -> Response:
    message, status_code, headers = health.run()
    return Response(content=message, headers=headers, status_code=status_code)


@router.get(
    "/health",
    summary="Check if this service is alive",
    description="Returns a simple message to indicate that this service is alive",
    tags=["health"],
)
def liveness() -> dict[str, str]:
    return {"message": "Ok"}
