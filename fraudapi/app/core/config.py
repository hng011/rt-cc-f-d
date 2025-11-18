from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    # APP
    project_name: str = "Credit Card Fraud Detector API"
    api_version: str = "beta"
    environment: str = "dev"
    debug: bool = False
    api_base_dir: str = "fraudapp"
    local_file_storage: str = "/tmp"
    log_level: str = "debug"
    host: str = "0.0.0.0"
    port: int = 8000
    
    # gcp
    google_project_id: Optional[str] = None
    gcs_bucket_location: Optional[str] = None
    gcs_bucket_name: Optional[str] = None
    
    # ML THINGS
    model_dir_path: str = "/models"
    model_filename: Optional[str] = None
    model_input_dim: int = 29
    model_threshold: float = ...

    # CORS
    cors_origins: list[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )

settings = Settings()