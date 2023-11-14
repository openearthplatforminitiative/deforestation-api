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
    api_description: str = 'This is a RESTful service that provides aggregated deforestation data over the period from 2001 to 2022 based on data provided by <a href="https://glad.umd.edu/">Global Land Analysis and Discovery (GLAD)</a> laboratory at the University of Maryland, in partnership with <a href="https://www.globalforestwatch.org/">Global Forest Watch (GFW)</a>. The data are freely available for use under a <a href="https://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.<br/><i>Citation: Hansen, M. C., P. V. Potapov, R. Moore, M. Hancher, S. A. Turubanova, A. Tyukavina, D. Thau, S. V. Stehman, S. J. Goetz, T. R. Loveland, A. Kommareddy, A. Egorov, L. Chini, C. O. Justice, and J. R. G. Townshend. 2013. High-Resolution Global Maps of 21st-Century Forest Cover Change. Science 342 (15 November): 850-53. Data available on-line from: <a href="https://glad.earthengine.app/view/global-forest-change">https://glad.earthengine.app/view/global-forest-change</a></i>.<br/><br/>The data provided by the `basin` endpoint are aggregated over river basin polygons provided by <a href="https://www.hydrosheds.org/products/hydrobasins">HydroSHEDS</a>. The basin data are feely available for non-commercial and commercial use under a licence agreement included in the <a href="https://data.hydrosheds.org/file/technical-documentation/HydroSHEDS_TechDoc_v1_4.pdf">HydroSHEDS Technical Documentation</a>.'


settings = Settings()
