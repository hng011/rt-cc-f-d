import numpy as np
import os
import logging
from typing import List

from fraudapi.core.config import settings
from fraudapi.core.storage import local_storage
from fraudapi.dto.request.transaction import (
    TransactionRequest,
    TransactionBatchRequest
)

from fraudapi.dto.response.prediction import (
    TransactionStatus,
    PredictionResponse,
    PredictionBatchResponse,
)


logger = logging.getLogger(__name__)


class PredictionService:
    
    def __init__(self):        
        self.model_path = local_storage.get_model_path(settings.model_filename)
        self.model = self._load_model()
        self.input_dim = settings.model_input_dim
        
        
    def _load_model(self):
        """
        Loads the model from the expected local file path.
        """
        
        import tensorflow as tf
        
        if not os.path.exists(self.model_path):
            logger.critical(f"FATAL: Model file not found at {self.model_path}. App startup likely failed.")
            return None
            
        try:
            logger.info(f"Loading model from local cache: {self.model_path}")
            model = tf.keras.models.load_model(self.model_path)
            logger.info("Model loaded successfully.")
            return model
        except Exception as e:
            logger.critical(f"FATAL ERROR: Could not load model from {self.model_path}. {e}", exc_info=True)
            return None


    def get_prediction(self, tx_request: TransactionRequest) -> PredictionResponse:
        """Calculates the reconstruction error (MAE)."""
        if not self.model:
            logger.error("Model is not loaded. Cannot make predictions.")
            raise RuntimeError("Model is not loaded. Cannot make predictions.")
        
        if len(tx_request.features) != self.input_dim:
            logger.warning(f"Invalid input. Expected {self.input_dim} features, got {len(tx_request.features)}")
            raise ValueError(f"Invalid input. Expected {self.input_dim} features, got {len(tx_request.features)}")
            
        input_data = np.array([tx_request.features])
        reconstructed_data = self.model.predict(input_data)
        mae = np.mean(np.abs(input_data - reconstructed_data), axis=1)[0]
        
        tx_status = TransactionStatus.FRAUD_RISK if mae > settings.model_threshold else TransactionStatus.NORMAL
        
        return PredictionResponse(
            autoencoder_error=mae,
            status=tx_status
        )


    def get_prediction_batch(self, batch_request: TransactionBatchRequest) -> PredictionBatchResponse:
        """
        Calculates reconstruction error for a whole batch of transactions
        by calling model.predict() only once.
        """
        if not self.model:
            logger.error("Model is not loaded. Cannot make predictions.")
            raise RuntimeError("Model is not loaded.")

        try:
            batch_features = []
            for tx in batch_request.transactions:
                if len(tx.features) != self.input_dim:
                    raise ValueError(f"Invalid transaction. Expected {self.input_dim} features.")
                batch_features.append(tx.features)
            
            input_batch = np.array(batch_features)

            reconstructed_batch = self.model.predict(input_batch)

            mae_list = np.mean(np.abs(input_batch - reconstructed_batch), axis=1)
            
            response_predictions: List[PredictionResponse] = []
            for error_score in mae_list:
                tx_status = TransactionStatus.NORMAL
                if error_score > settings.model_threshold:
                    tx_status = TransactionStatus.FRAUD_RISK
                
                response_predictions.append(
                    PredictionResponse(autoencoder_error=float(error_score), status=tx_status)
                )
            
            return PredictionBatchResponse(transactions=response_predictions)

        except ValueError as e:
            logger.warning(f"Batch prediction failed validation: {e}")
        except Exception as e:
            logger.error(f"Batch prediction failed: {e}", exc_info=True)
        
        
prediction_service = PredictionService()