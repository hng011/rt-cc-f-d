from typing import List, Literal
from pydantic import BaseModel
from enum import Enum


class TransactionStatus(Enum):
    FRAUD_RISK = "FRAUD_RISK"
    NORMAL = "NORMAL"


class PredictionResponse(BaseModel):
    autoencoder_error: float
    status: TransactionStatus


class PredictionBatchResponse(BaseModel):
    transactions: List[PredictionResponse]