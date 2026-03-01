import logging
from functools import wraps
from typing import Callable, Any
from colorlog import ColoredFormatter


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    formatter = ColoredFormatter(
        "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


def log(logger: logging.Logger):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            logger.info(f"Calling {func.__name__} with args: {args}, kwargs: {kwargs}")
            try:
                result = await func(*args, **kwargs)
                logger.info(f"{func.__name__} completed successfully")
                return result
            except Exception as e:
                logger.exception(f"Error in {func.__name__}: {str(e)}")
                raise
        return wrapper
    return decorator


