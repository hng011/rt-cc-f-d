import logging

from fastapi import (
    APIRouter,
    HTTPException
)

from app.dto.request.transaction import (
    TransactionRequest,
    TransactionBatchRequest,
)


tag = __name__.split('.')[-1]
logger = logging.getLogger(tag)
router = APIRouter(
    prefix=f"/{tag}",
    tags=[tag]
)


@router.get("/sanityCheck")
def sanity_check():
    return f"{tag} fine"


@router.post("/")
def get_prediction(tx: TransactionRequest):
    try:        
        from app.service.prediction_service import prediction_service
        
        return prediction_service.get_prediction(tx)
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Internal server error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
    
    
@router.post("/batch")
def get_prediction_batch(txs: TransactionBatchRequest):
    try:        
        from app.service.prediction_service import prediction_service
        
        return prediction_service.get_prediction_batch(txs)
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Internal server error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")