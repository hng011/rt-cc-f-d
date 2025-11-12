import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fraudapi.api.base import api_router

from fraudapi.core.logging import setup_logging
from fraudapi.core.config import settings
from fraudapi.core.storage import gcs_storage_service
import os

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.project_name,
    version=settings.api_version,
    debug=settings.debug
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)


# REGISTER BASE API
app.include_router(api_router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    """Log app startup"""
    logger.info(f"Starting {settings.project_name} v{settings.api_version}")
    
    """Download model"""
    gcs_storage_service.download_model_file(
        model_filename=os.path.join(settings.model_filename)
    )
    
    
@app.get("/", tags=["status"])
def read_root():
    """Root endpoint to check if the API is live."""
    logger.info("Health check endpoint was hit.")
    return {"status": f"{settings.project_name} is running"}
