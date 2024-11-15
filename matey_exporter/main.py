
import os
import time
import asyncio
from requests.exceptions import ConnectionError

from matey_exporter.utils import get_config, load_sources
from prometheus_client import Summary
from .logger import logger


async def async_start_matey_exporter(sources: set, interval: int) -> None:
    '''Main async function'''
    
    sleep_time = interval
    matey_exporter_data_query_time_seconds = Summary('matey_exporter_data_query_time_seconds', 
                                                     'Latency for Matey exporter to complete query', 
                                                      labelnames=['job'])
    while True:
        
        start_time = time.time()
        try:
            async with asyncio.timeout(5):
                await_tasks = set()
                
                # Gather all tasks from sources and run them concurrently.
                # In Python <3.13 this will only improve performance for
                # api calls within a thread, but might gain better performance
                # from future Python version with unlocked GIL.
                for source in sources: await_tasks.add(asyncio.to_thread(source.query_and_process_data))
                
                # Wait for all tasks to complete
                await asyncio.gather(*await_tasks)
    
        except TimeoutError: # TODO: Make timeouts non-blocking
            logger.info("One or more datasources timed out.")
        
        except ConnectionError as e: # TODO: remove source and log error
            logger.info(f"Connection error: {e}")

        # TODO: Evaluate what operations should be timed.
        matey_exporter_data_query_time_seconds.labels('matey_exporter').observe(time.time() - start_time)
        await asyncio.sleep(sleep_time)


def start_matey_exporter(config_file: str, interval: int) -> None:
    '''Start Matey exporter main data collection loop'''
    
    config = get_config(config_file)
    sources = load_sources(config)
    asyncio.run(async_start_matey_exporter(sources=sources, interval=interval))