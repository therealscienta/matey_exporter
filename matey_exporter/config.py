from pathlib import Path
from dataclasses import dataclass
from matey_exporter.common.decorators import singleton


class MateyExporterDefaultConfig:
    '''Default configuration for Matey Exporter'''
    CONFIG_FILE :str = Path(Path(__file__).parent.parent) / 'config.yaml'
    LOGLEVEL :str = 'INFO'
    PORT :int = 8000
    INTERVAL :int = 30


@singleton
@dataclass
class MateyExporterConfig:
    '''
    Global Singleton Configuration Class for Matey Exporter.
    Can be accessed globally via MateyExporterConfig(), and
    is used to configure the exporter and collectors.
    
    :param loglevel: Log level for logging.
    :param port: Port to listen for HTTP traffic.
    :param interval: Interval between data collection jobs.
    :param config_file: Path to config file.
    '''
    loglevel :str = MateyExporterDefaultConfig.LOGLEVEL
    port :int = MateyExporterDefaultConfig.PORT
    interval :int = MateyExporterDefaultConfig.INTERVAL
    config_file :str = MateyExporterDefaultConfig.CONFIG_FILE

# TODO: Create configuration classes for each collector 
# to enable or disable specific metrics.

# @dataclass
# class MateyTransmissionCollectorConfig:
#     '''Configuration for Transmission collector'''
#     track_ratio :bool = True
#     track_download_speed :bool = True
#     track_upload_speed :bool = True
#     track_downloaded_ever :bool = True
#     track_uploaded_ever :bool = True
#     track_file_count :bool = True
#     track_torrent_count :bool = True
#     track_active_torrent_count :bool = True
    