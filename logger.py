import logging
import sys
import os

def get_logger(name="xml_processor", log_file: str = None, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent adding multiple handlers
    if not getattr(logger, "has_been_configured", False):

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler (if log_file is given)
        if log_file:
            folder = os.path.dirname(log_file)
            if folder:
                os.makedirs(folder, exist_ok=True)
            file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)


        # Mark as configured to avoid duplicate handlers
        logger.has_been_configured = True

    return logger
