
import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

from prometheus_client import start_http_server, Info
from matey_exporter import MateyExporterConfig, start_matey_exporter, logger, __version__

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
    
    mateyconfig = MateyExporterConfig()
    
    # Get listening port from arguments, or environment or default to 8000.
    if (http_port := args.port) or (http_port := os.environ.get('PORT')):
        mateyconfig.port = int(http_port)
    
    # TODO: Handle both provided dir or file as input.
    # Get config file path from args or environment or default to config.yaml in the same directory as this script.
    if (config_file := args.config) or (config_file := os.environ.get('CONFIG_PATH')):
        mateyconfig.config_file = Path(config_file)
    
    # Get log level from args or environment or default to INFO.
    if (logging_level := args.log_level) or (logging_level := os.environ.get('LOGLEVEL')):
        mateyconfig.loglevel = logging_level
    logger.setLevel(mateyconfig.loglevel.upper())
    
    #  Get interval from args or environment or default to 30 seconds.
    if (interval := args.interval) or (interval := os.environ.get('INTERVAL')): 
        mateyconfig.interval = int(interval)
    
    # Set the version of the exporter. Build version supplied by CI pipeline.
    i = Info('matey_build_version', 'Prometheus Matey Exporter build version')
    i.info({'version': __version__, 'build': 'XXXXXXXX'})
    
    if mateyconfig.loglevel.upper() == 'DEBUG':
        logger.debug(f'Matey exporter config: {mateyconfig}')
    
    # Start up the server to expose the metrics.
    # TODO: Handle KeyboardInterrupt (http servers are not nicely shutdown)
    logger.info('Matey exporter starting.')
    try:
        start_http_server(mateyconfig.port)
        start_matey_exporter()
    except (OSError, PermissionError) as e:
        logger.error(f'Failed to start server: {e}')
    except KeyboardInterrupt:
        logger.error(f'Matey exporter was interrupted.')
    except Exception as e:
        logger.error(f'Unexpected error: {e}')
    finally:
        sys.exit(1)
