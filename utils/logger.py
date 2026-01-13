import os
import sys
from loguru import logger

# Create logs directory if it doesn't exist
log_dir = "logs"
if not os.path.exists(log_dir):
    try:
        os.makedirs(log_dir)
    except OSError as e:
        # Fallback to stderr if we can't create directory
        print(f"Error creating log directory: {e}", file=sys.stderr)

# Configure logger
# We remove the default handler to avoid duplicates if re-imported (though Streamlit caching usually prevents this)
# However, loguru's default handler is ID 0.
try:
    logger.remove(0) 
except ValueError:
    pass # Handler might have been removed already

# Add console handler (stderr) with color
logger.add(sys.stderr, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")

# Add file handler
log_file_path = os.path.join(log_dir, "hopon.log")
logger.add(log_file_path, rotation="5 MB", retention="10 days", compression="zip", level="INFO", mode="w")

def get_logger():
    return logger

# Log that the logger is initialized
logger.info("Logger initialized.")
