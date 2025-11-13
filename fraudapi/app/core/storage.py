import os
import logging
from pathlib import Path
from google.cloud import storage
from app.core.config import settings

logger = logging.getLogger(__name__)

class GCSStorageService:
    """
    A base service for all Google Cloud Storage operations.
    """
    
    def __init__(self):                
        try:
            self.client = storage.Client()
            self.bucket = self.client.bucket(settings.gcs_bucket_name)
            logger.info(f"GCSStorageService ({self.bucket.name}) initialized successfully.")
        except Exception as e:
            logger.critical(f"FATAL ERROR: Could not initialize GCS Client. {e}", exc_info=True)
            self.client = None
            

    def download_model_file(self, model_filename: str) -> str:
        """
        Downloads a file from GCS to the app's standard cache path.
        
        Returns:
            The local path of the downloaded file.
        """
        if not self.client:
            logger.error("GCS Client is not initialized. Download failed.")
            raise RuntimeError("GCS Client is not initialized.")
                    
        try:
            source_blob_name = os.path.join(
                settings.app_base_dir, 
                settings.model_dir_path, 
                model_filename
            )
            
            local_destination_path = os.path.join(
                settings.local_file_storage,
                source_blob_name,
            )
            
            local_dir = os.path.dirname(local_destination_path)  
            os.makedirs(local_dir, exist_ok=True)
            
            if source_blob_name.split("/")[-1] in os.listdir(local_dir):
                logger.info(f"{local_destination_path} already exsist")
            else:
                
                # replace exisisting file (if available) with a new file
                for item in Path(local_dir).iterdir():
                    if item and item.is_file():
                        logger.info(f"deleting {item}")
                        item.unlink()
                            
                logger.info(f"Downloading gs://{self.bucket.name}/{source_blob_name} to {local_destination_path}...")
                blob = self.bucket.blob(source_blob_name)
                blob.download_to_filename(local_destination_path)
                
                logger.info(f"File downloaded successfully to {local_destination_path}")
                
            return local_destination_path
            
        except Exception as e:
            logger.error(f"ERROR: Failed to download file. {e}", exc_info=True)


class LocalStorage:
    """
    Manages the local file cache paths for the application.
    """
    def __init__(self):
        self.local_file_storage = os.path.join(settings.local_file_storage, settings.app_base_dir)
        logger.info(f"LocalStorage initialized. Base path: {self.local_file_storage}")

    def get_model_path(self, model_filename: str) -> str:
        """
        Gets the full, expected local path for a given model file.
        """
        model_path = os.path.join(
            self.local_file_storage,
            settings.model_dir_path,
            model_filename   
        )
        
        return model_path

gcs_storage_service = GCSStorageService()
local_storage = LocalStorage()