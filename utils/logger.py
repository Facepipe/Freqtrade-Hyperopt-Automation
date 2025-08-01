import logging
from pathlib import Path

def setup_logging(log_file: Path) -> logging.Logger:
    logger = logging.getLogger("hyperopt_automation")
    logger.setLevel(logging.INFO)
    logger.handlers = []
    
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger