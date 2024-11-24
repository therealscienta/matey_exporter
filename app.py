
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
    
    # Get listening port from arguments, or environment or default to 8000.
    if not (http_port := args.port):
        http_port = int(os.environ.get('PORT', MateyExporterConfig.DEFAULT_PORT))
    
    # TODO: Handle both provided dir or file as input.
    # Get config file path from args or environment or default to config.yaml in the same directory as this script.
    if (config_file := args.config) or (config_file := os.environ.get('CONFIG_PATH')):
        config_file = Path(config_file)
    else:
        config_file = MateyExporterConfig.DEFAULT_CONFIG_FILE
    
    # Get log level from args or environment or default to INFO.
    if not (logging_level := args.log_level):
        logging_level = os.environ.get('LOGLEVEL', MateyExporterConfig.DEFAULT_LOGLEVEL)
    logger.setLevel(logging_level.upper())
    
    #  Get interval from args or environment or default to 30 seconds.
    if not (interval := args.interval): 
        interval = int(os.environ.get('INTERVAL', MateyExporterConfig.DEFAULT_INTERVAL))
    
    # Set the version of the exporter. Build version supplied by CI pipeline.
    i = Info('matey_build_version', 'Prometheus Matey Exporter build version')
    i.info({'version': __version__, 'build': 'XXXXXXXX'})
    
    # Start up the server to expose the metrics.
    # TODO: Handle KeyboardInterrupt (http servers are not nicely shutdown)
    logger.info('Matey exporter starting.')
    try:
        start_http_server(http_port)
        start_matey_exporter(config_file=config_file, interval=interval)
    except (OSError, PermissionError) as e:
        logger.error(f'Failed to start server: {e}')
    except KeyboardInterrupt:
        logger.error(f'Matey exporter was interrupted.')
    except Exception as e:
        logger.error(f'Unexpected error: {e}')
    finally:
        sys.exit(1)
