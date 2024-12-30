
import time
from prometheus_client import Gauge, Summary, Enum
import qbittorrentapi

from matey_exporter.common.exceptions import MateyQueryAndProcessDataError
from matey_exporter.common.decorators import singleton
from matey_exporter.common.base import BaseMateyClass

STATES = [
    'error',
    'missingFiles',
    'allocating',
    'checkingResumeData',
    'moving',
    'metaDL', 
    'unknown',
    'uploading',
    'downloading',
    'stalledUP',
    'stalledDL',
    'checkingUP',
    'checkingDL',
    'forcedUP',
    'forcedDL',
    'pausedUP',
    'pausedDL',
    'queuedUP',
    'queuedDL',
    'stoppedUP', # The stopped states are not included in the API docs,
    'stoppedDL', # but was found during testing.
]

@singleton        
class MateyQbittorrentPrometheusMetrics:
    def __init__(self):
        
        self.qbittorrent_torrent_state = Enum(
            name='qbittorrent_torrent_state',
            documentation='Available Qbittorrent Torrent states', 
            labelnames=['instance', 'torrent_name', 'torrent_path'],
            states=STATES)
        
        self.qbittorrent_torrent_ratio = Gauge(
            name='qbittorrent_torrent_ratio',
            documentation='Qbittorrent Torrent ratio', 
            labelnames=['instance', 'torrent_name', 'torrent_path'])
        
        self.qbittorrent_torrent_total_size_bytes = Gauge(
            name='qbittorrent_torrent_total_size_bytes',
            documentation='Qbittorrent Torrent total size', 
            labelnames=['instance', 'torrent_name', 'torrent_path'])

        self.qbittorrent_torrent_uploaded_bytes = Gauge(
            name='qbittorrent_torrent_uploaded_bytes',
            documentation='Qbittorrent Torrent uploaded in bytes', 
            labelnames=['instance', 'torrent_name', 'torrent_path'])

        self.qbittorrent_torrent_downloaded_bytes = Gauge(
            name='qbittorrent_torrent_downloaded_bytes',
            documentation='Qbittorrent Torrent completed in bytes', 
            labelnames=['instance', 'torrent_name', 'torrent_path'])

        self.qbittorrent_torrent_dlspeed = Gauge(
            name='qbittorrent_torrent_dlspeed',
            documentation='Qbittorrent Torrent download speed', 
            labelnames=['instance', 'torrent_name', 'torrent_path'])
        
        self.qbittorrent_torrent_ulspeed = Gauge(
            name='qbittorrent_torrent_ulspeed',
            documentation='Qbittorrent Torrent upload speed', 
            labelnames=['instance', 'torrent_name', 'torrent_path'])
        
        self.qbittorrent_torrent_time_active_seconds = Gauge(
            name='qbittorrent_torrent_time_active_seconds',
            documentation='Qbittorrent Torrent active seconds', 
            labelnames=['instance', 'torrent_name', 'torrent_path'])

        self.qbittorrent_torrent_tracker_count = Gauge(
            name='qbittorrent_torrent_tracker_count',
            documentation='Qbittorrent Torrent active trackers', 
            labelnames=['instance', 'torrent_name', 'torrent_path'])
        
        self.qbittorrent_torrent_priority = Gauge(
            name='qbittorrent_torrent_priority',
            documentation='Qbittorrent Torrent priority', 
            labelnames=['instance', 'torrent_name', 'torrent_path'])

        self.qbittorrent_api_query_latency_seconds = Summary(
            name='qbittorrent_api_query_latency_seconds',
            documentation='Latency for a single API query',
            labelnames=['instance'])
        
        self.qbittorrent_data_processing_latency_seconds = Summary(
            name='qbittorrent_data_processing_latency_seconds',
            documentation='Latency for exporter data processing',
            labelnames=['instance'])

    
class MateyQbittorrent(BaseMateyClass):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api = qbittorrentapi.Client(**{
                        'host': self.host_url, 
                        'username' : kwargs.get('username'), 
                        'password' : kwargs.get('password')})
    
        self.api.VERIFY_WEBUI_CERTIFICATE = kwargs.get('verify')
        self.metrics = MateyQbittorrentPrometheusMetrics()

    def get_torrent_data(self) -> None:
        '''
        Query qBittorrent API for torrent data and process results.
        '''
        
        start_api_query_latency_time = time.time()
        api_data = self.api.torrents_info()
        self.metrics.qbittorrent_api_query_latency_seconds.labels(
            self.instance_name).observe(time.time() - start_api_query_latency_time)
        
        start_data_processing_latency_time = time.time()
        for torrent in api_data:
            
            self.metrics.qbittorrent_torrent_state.labels(
                instance=self.instance_name,
                torrent_name=torrent.name,
                torrent_path=torrent.content_path).state(torrent.state)
            
            self.metrics.qbittorrent_torrent_ratio.labels(
                instance=self.instance_name,
                torrent_name=torrent.name,
                torrent_path=torrent.content_path).set(torrent.ratio)

            self.metrics.qbittorrent_torrent_total_size_bytes.labels(
                instance=self.instance_name,
                torrent_name=torrent.name,
                torrent_path=torrent.content_path).set(torrent.total_size)

            self.metrics.qbittorrent_torrent_uploaded_bytes.labels(
                instance=self.instance_name,
                torrent_name=torrent.name,
                torrent_path=torrent.content_path).set(torrent.uploaded)

            self.metrics.qbittorrent_torrent_downloaded_bytes.labels(
                instance=self.instance_name,
                torrent_name=torrent.name,
                torrent_path=torrent.content_path).set(torrent.downloaded)

            self.metrics.qbittorrent_torrent_dlspeed.labels(
                instance=self.instance_name,
                torrent_name=torrent.name,
                torrent_path=torrent.content_path).set(torrent.dlspeed)

            self.metrics.qbittorrent_torrent_ulspeed.labels(
                instance=self.instance_name,
                torrent_name=torrent.name,
                torrent_path=torrent.content_path).set(torrent.upspeed)

            self.metrics.qbittorrent_torrent_time_active_seconds.labels(
                instance=self.instance_name,
                torrent_name=torrent.name,
                torrent_path=torrent.content_path).set(torrent.time_active)

            self.metrics.qbittorrent_torrent_tracker_count.labels(
                instance=self.instance_name,
                torrent_name=torrent.name,
                torrent_path=torrent.content_path).set(torrent.trackers_count)
            
            self.metrics.qbittorrent_torrent_priority.labels(
                instance=self.instance_name,
                torrent_name=torrent.name,
                torrent_path=torrent.content_path).set(torrent.priority)
        
        self.metrics.qbittorrent_data_processing_latency_seconds.labels(
            self.instance_name).observe(time.time() - start_data_processing_latency_time)
                                        

    def query_and_process_data(self) -> None:
        '''
        Run all query and process methods in the Qbittorrent instance
        '''
        
        try:
            self.get_torrent_data()
        except Exception as e:
            raise MateyQueryAndProcessDataError(self.instance_name, e)
