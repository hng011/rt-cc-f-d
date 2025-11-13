import logging
import sys
from app.core.config import settings

def setup_logging():
    """
    Configures the root logger for the application.
    This should be called ONCE at startup.
    """
    log_level = settings.log_level.upper()

    logging.basicConfig(
        level=log_level,
        stream=sys.stdout,
        format="[%(levelname)s]:\t %(asctime)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    logging.getLogger(__name__).info(f"Logger configured with level: {log_level}")  