from fastapi import APIRouter
from fraudapi.api.endpoint import (
    prediction,
)


api_router = APIRouter()
api_router.include_router(prediction.router)