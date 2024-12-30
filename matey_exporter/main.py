import time
import asyncio
from prometheus_client import Summary

from matey_exporter.utils import get_config, load_sources
from matey_exporter.common.log import logger
from matey_exporter.config import MateyExporterConfig

async def async_start_matey_exporter(sources: set, interval: int) -> None:
    '''Main async function'''
    
    sleep_time = interval
    matey_exporter_data_query_time_seconds = Summary('matey_exporter_data_query_time_seconds', 
                                                     'Latency for Matey exporter to complete query', 
                                                      labelnames=['job'])
    while True:
        
        try:
            start_time = time.time()
            await_tasks = set()
                    
            # Gather all tasks from sources and run them concurrently.
            # In Python <3.13 this will only improve performance for
            # api calls within a thread, but might gain better performance
            # from future Python version with unlocked GIL.
            for source in sources: await_tasks.add(asyncio.to_thread(source.query_and_process_data))
                   
            # Wait for all tasks to complete
            await asyncio.gather(*await_tasks)

            # TODO: Evaluate what operations should be timed.
            matey_exporter_data_query_time_seconds.labels('matey_exporter').observe(time.time() - start_time)
        
        except Exception as e:
            logger.error(e)
        
        await asyncio.sleep(sleep_time)


def start_matey_exporter() -> None:
    '''Start Matey exporter main data collection loop'''
    
    mateyconfig = MateyExporterConfig()
    config = get_config(mateyconfig.config_file)
    sources = load_sources(config)
    
    sources_loaded = '\n'.join(
        [str(f'-\t{source.instance_name}: {source.host_url}') for source in sources])
    
    logger.info(f'Loaded sources: \n{sources_loaded}')
    
    asyncio.run(async_start_matey_exporter(
        sources=sources, interval=mateyconfig.interval))