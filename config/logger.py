import logging
import sys

def setup_logger(debug_mode=True):
    """
    Configures and returns a centralized logger for the application.
    """
    logger = logging.getLogger("CompressionApp")
    
    # Avoid adding multiple handlers if setup is called multiple times
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG if debug_mode else logging.INFO)
        
        # Create console handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG if debug_mode else logging.INFO)
        
        # Create formatter and add it to the handler
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        ch.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(ch)
        
    return logger

# Create a default instance to be imported across modules
logger = setup_logger(debug_mode=True)
