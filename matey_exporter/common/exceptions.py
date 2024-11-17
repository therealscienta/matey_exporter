
from requests.exceptions import ConnectionError
from .logger import logger


def exception_handler(func):
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ConnectionError as e:
            logger.error(f"{func.__name__} failed to connect to the server: {e}")
        except Exception as e:
            logger.error(f"Something went wrong: {e}")
    return inner_function
