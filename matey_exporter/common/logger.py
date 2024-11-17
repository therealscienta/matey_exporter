import logging

# Set up a logger
logger = logging.getLogger('matey_exporter')

# Set up a stream handler to log to the console
stream_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
stream_handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(stream_handler)
