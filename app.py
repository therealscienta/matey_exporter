
import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

from matey_exporter import start_matey_exporter, logger
from prometheus_client import start_http_server, Info


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(
        add_help=True,
        description="Matey Exporter is a Prometheus exporter for all things \
                    a virtual sailor of the seven seas might need.")
    
    parser.add_argument('--config',    type=str, help="Path to config file.")
    parser.add_argument('--port',      type=int, help="Port to listen for HTTP traffic.")
    parser.add_argument('--interval',  type=int, help="Interval between data collection jobs.")
    parser.add_argument('--log_level',    
                        type=str, choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], 
                        help="Log level, default: INFO.")

    args = parser.parse_args()
    load_dotenv()
    
    # Get listening port from arguments, or environment or default to 8000.
    if not (http_port := args.port): http_port = int(os.environ.get('PORT', 8000))
    
    # Get config file path from args or environment or default to config.yaml in the same directory as this script.
    if not (config_file := args.config) or not (config_file := Path(os.environ.get('CONFIG_PATH'))):
        parent = Path(__file__).parent
        config_file = Path(parent) / 'config.yaml'
    
    # Get log level from args or environment or default to INFO.
    if not (logging_level := args.log_level): logging_level = os.environ.get('LOGLEVEL', 'INFO').upper()
    logger.setLevel(logging_level)
    
    #  Get interval from args or environment or default to 30 seconds.
    if not (interval := args.interval): interval = int(os.environ.get('INTERVAL', 30))
    
    # Start up the server to expose the metrics.
    i = Info('matey_build_version', 'Prometheus Matey Exporter build version')
    i.info({'version': 'X.X', 'build': 'XXXXXXXX'})
    logger.info('Matey exporter starting.')
    
    # TODO: Handle KeyboardInterrupt (http servers are not nicely shutdown)
    try:
        start_http_server(http_port)
        start_matey_exporter(config_file=config_file, interval=interval)
    except KeyboardInterrupt:
        sys.exit('Matey exporter was interrupted.')
