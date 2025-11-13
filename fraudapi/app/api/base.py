from fastapi import APIRouter
from app.api.endpoint import (
    prediction,
)


api_router = APIRouter()
api_router.include_router(prediction.router)