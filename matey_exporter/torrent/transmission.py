
import time
from prometheus_client import Gauge, Summary, Enum
from transmission_rpc import Client

from matey_exporter.common import MateyQueryAndProcessDataError, singleton, BaseMateyClass

STATES = [
    'check pending',
    'checking',
    'downloading',
    'download pending',
    'seeding',
    'seed pending', 
    'stopped',
]


@singleton
class MateyTransmissionPrometheusMetrics:
    def __init__(self):
        
        self.transmission_torrent_state = Enum(
            name='transmission_torrent_state',
            documentation='Available Transmission Torrent states',
            labelnames=['instance', 'torrent_name', 'torrent_path'],
            states=STATES)

        self.transmission_torrent_error = Gauge(
            name='transmission_torrent_error',
            documentation='Transmission torrent error',
            labelnames=['instance', 'torrent_name', 'torrent_path'])
        
        self.transmission_torrent_ratio = Gauge(
            name='transmission_torrent_ratio',
            documentation='Transmission torrent ratio',
            labelnames=['instance', 'torrent_name', 'torrent_path'])

        self.transmission_torrent_download_speed_bytes = Gauge(
            name='transmission_torrent_download_speed_bytes',
            documentation='Transmission torrent download speed',
            labelnames=['instance', 'torrent_name', 'torrent_path'])

        self.transmission_torrent_upload_speed_bytes = Gauge(
            name='transmission_torrent_upload_speed_bytes',
            documentation='Transmission torrent upload speed',
            labelnames=['instance', 'torrent_name', 'torrent_path'])

        self.transmission_torrent_total_size_bytes = Gauge(
            name='transmission_torrent_total_size_bytes',
            documentation='Transmission torrent total size',
            labelnames=['instance', 'torrent_name', 'torrent_path'])

        self.transmission_torrent_downloaded_bytes = Gauge(
            name='transmission_torrent_downloaded_bytes',
            documentation='Transmission torrent downloaded',
            labelnames=['instance', 'torrent_name', 'torrent_path'])
        
        self.transmission_torrent_uploaded_bytes = Gauge(
            name='transmission_torrent_uploaded_bytes',
            documentation='Transmission torrent uploaded',
            labelnames=['instance', 'torrent_name', 'torrent_path'])
        
        self.transmission_torrent_trackers = Gauge(
            name='transmission_torrent_trackers',
            documentation='Transmission torrent trackers',
            labelnames=['instance', 'torrent_name', 'torrent_path'])
        
        self.transmission_torrent_file_count = Gauge(
            name='transmission_torrent_file_count',
            documentation='Transmission torrent file count',
            labelnames=['instance', 'torrent_name', 'torrent_path'])
        
        self.transmission_api_query_latency_seconds = Summary(
            name='transmission_api_query_latency_seconds',
            documentation='Latency for a single API query',
            labelnames=['instance'])
        
        self.transmission_data_processing_latency_seconds = Summary(
            name='transmission_data_processing_latency_seconds',
            documentation='Latency for exporter data processing',
            labelnames=['instance'])

    
class MateyTransmission(BaseMateyClass):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api = Client(
            host=kwargs.get('host_url').replace('http://', ''), # TODO: Remove replace and fix URL parsing in config. Client does not want http://
            username=kwargs.get('username'), 
            password=kwargs.get('password'))
        self.api._http_session.verify = kwargs.get('verify') # Disable SSL verification
        self.metrics = MateyTransmissionPrometheusMetrics()

    def get_torrent_data(self) -> None:
        '''
        Query Transmission API for torrent data and process results.
        '''

        start_api_query_latency_time = time.time()
        data = self.api.get_torrents()
        self.metrics.transmission_api_query_latency_seconds.labels(
            self.instance_name).observe(time.time() - start_api_query_latency_time)
        
        start_data_processing_latency_time = time.time()
        
        for torrent in data:
            self.metrics.transmission_torrent_state.labels(
                instance=self.instance_name,
                torrent_name=torrent.name,
                torrent_path=torrent.download_dir).state(torrent.status)
            
            self.metrics.transmission_torrent_error.labels(
                instance=self.instance_name,
                torrent_name=torrent.name,
                torrent_path=torrent.download_dir).set(torrent.error)

            self.metrics.transmission_torrent_ratio.labels(
                instance=self.instance_name,
                torrent_name=torrent.name,
                torrent_path=torrent.download_dir).set(torrent.ratio)

            self.metrics.transmission_torrent_download_speed_bytes.labels(
                instance=self.instance_name,
                torrent_name=torrent.name,
                torrent_path=torrent.download_dir).set(torrent.rate_download)

            self.metrics.transmission_torrent_upload_speed_bytes.labels(
                instance=self.instance_name,
                torrent_name=torrent.name,
                torrent_path=torrent.download_dir).set(torrent.rate_upload)

            self.metrics.transmission_torrent_total_size_bytes.labels(
                instance=self.instance_name,
                torrent_name=torrent.name,
                torrent_path=torrent.download_dir).set(torrent.total_size)

            self.metrics.transmission_torrent_trackers.labels(
                instance=self.instance_name,
                torrent_name=torrent.name,
                torrent_path=torrent.download_dir).set(len(torrent.tracker_list))
            
            self.metrics.transmission_torrent_downloaded_bytes.labels(
                instance=self.instance_name,
                torrent_name=torrent.name,
                torrent_path=torrent.download_dir).set(torrent.downloaded_ever)
            
            self.metrics.transmission_torrent_uploaded_bytes.labels(
                instance=self.instance_name,
                torrent_name=torrent.name,
                torrent_path=torrent.download_dir).set(torrent.uploaded_ever)
            
            self.metrics.transmission_torrent_file_count.labels(
                instance=self.instance_name,
                torrent_name=torrent.name,
                torrent_path=torrent.download_dir).set(torrent.file_count)

        self.metrics.transmission_data_processing_latency_seconds.labels(
            self.instance_name).observe(time.time() - start_data_processing_latency_time)
                                        

    def query_and_process_data(self) -> None:
        '''Run all query and process methods in the Transmission instance'''
        try:
            self.get_torrent_data()
        except Exception as e:
            raise MateyQueryAndProcessDataError(self.instance_name, e)

