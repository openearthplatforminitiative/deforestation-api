from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    version: str = "0.0.1"
    uvicorn_port: int = 8080
    uvicorn_host: str = "0.0.0.0"
    uvicorn_reload: bool = True
    uvicorn_proxy_headers: bool = False
    basin_data_path: str = "s3://databricks-data-openepi/deforestation/basins.parquet"
    lossyear_data_path: str = "s3://databricks-data-openepi/deforestation/lossyear.parquet"
    api_root_path: str = "/"


settings = Settings()
