from typing import List
from pydantic import BaseModel


class TransactionRequest(BaseModel):
    features: List[float]

    
class TransactionBatchRequest(BaseModel):
    transactions: List[TransactionRequest]