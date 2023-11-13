from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    version: str = "0.0.1"
    uvicorn_port: int = 8080
    uvicorn_host: str = "0.0.0.0"
    uvicorn_reload: bool = True
    uvicorn_proxy_headers: bool = False
    basin_data_path: str = "s3://databricks-data-openepi/deforestation/basins.parquet"
    lossyear_data_path: str = (
        "s3://databricks-data-openepi/deforestation/lossyear.parquet"
    )
    api_root_path: str = "/"
    api_description: str = 'This is a RESTful service that provides aggregated deforestation data over the period from 2001 to 2022 based on data sourced from: <a href="https://glad.earthengine.app/view/global-forest-change">https://glad.earthengine.app/view/global-forest-change</a>.<br/>The data are freely available for use under a <a href="https://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>. <br/><br/><b>Source</b>: Hansen, M. C., P. V. Potapov, R. Moore, M. Hancher, S. A. Turubanova, A. Tyukavina, D. Thau, S. V. Stehman, S. J. Goetz, T. R. Loveland, A. Kommareddy, A. Egorov, L. Chini, C. O. Justice, and J. R. G. Townshend. 2013. High-Resolution Global Maps of 21st-Century Forest Cover Change. Science 342 (15 November): 850-53. Data available on-line from: <a href="https://glad.earthengine.app/view/global-forest-change">https://glad.earthengine.app/view/global-forest-change</a>.'


settings = Settings()
