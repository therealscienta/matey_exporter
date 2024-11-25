
import time
from prometheus_client import Gauge, Summary
from transmission_rpc import Client

from matey_exporter.common import MateyQueryAndProcessDataError, singleton
from .base import BaseTorrentClass

@singleton
class MateyTransmissionPrometheusMetrics:
    def __init__(self):
        self.check_pending_torrents =       Gauge('check_pending_torrents',      'Number of check pending torrents',    labelnames=['instance'])
        self.checking_torrents =            Gauge('checking_torrents',           'Number of checking torrents',         labelnames=['instance'])
        self.downloading_torrents =         Gauge('downloading_torrents',        'Number of downloading torrents',      labelnames=['instance'])
        self.download_pending_torrents =    Gauge('download_pending_torrents',   'Number of download pending torrents', labelnames=['instance'])
        self.seeding_torrents =             Gauge('seeding_torrents',            'Number of seeding torrents',          labelnames=['instance'])
        self.seed_pending_torrents =        Gauge('seed_pending_torrents',       'Number of seed pending torrents',     labelnames=['instance'])
        self.stopped_torrents =             Gauge('stopped_torrents',            'Number of stopped torrents',          labelnames=['instance'])
        
        self.transmission_api_query_latency_seconds =         Summary('transmission_api_query_latency_seconds',       'Latency for a single API query',       labelnames=['instance'])
        self.transmission_data_processing_latency_seconds =   Summary('transmission_data_processing_latency_seconds', 'Latency for exporter data processing', labelnames=['instance'])

transmission_metrics = MateyTransmissionPrometheusMetrics()
    
class MateyTransmission(BaseTorrentClass):
    
    def __init__(self, **kwargs):
        super().__init__(Client(kwargs.get('host_url'), kwargs.get('api_key')), **kwargs)
        self.api._http_session = kwargs.get('verify') # TODO: Using private attribute
        self.metrics = transmission_metrics


    def filter_data(data: dict) -> dict:
        '''
        Filter returned torrent data based on state of torrent. 
        Dictionary keys are based on states from official API documentation:
        https://transmission-rpc.readthedocs.io/en/v7.0.11/torrent.html#transmission_rpc.Torrent.status
        '''
        data_dict = {
            'check pending': 0,
            '‘checking’': 0,
            '‘downloading’': 0,
            'download pending': 0,
            '‘seeding’': 0,
            'seed pending': 0, 
            'stopped': 0,
        }
        for d in data: data_dict[d.get('status')] += 1
        return data_dict


    def get_torrent_data(self) -> None:
        '''
        Query Transmission API for torrent data and process results.
        '''

        start_api_query_latency_time = time.time()
        data = self.api.get_torrents()
        self.metrics.transmission_api_query_latency_seconds.labels(self.instance_name).observe(time.time() - start_api_query_latency_time)
        
        start_data_processing_latency_time = time.time()
        filtered_data = self.filter_data(data)
        
        self.metrics.check_pending_torrents.labels(self.instance_name).set(filtered_data.get('check pending'))
        self.metrics.checking_torrents.labels(self.instance_name).set(filtered_data.get('checking'))
        self.metrics.downloading_torrents.labels(self.instance_name).set(filtered_data.get('downloading'))
        self.metrics.download_pending_torrents.labels(self.instance_name).set(filtered_data.get('download pending'))
        self.metrics.seeding_torrents.labels(self.instance_name).set(filtered_data.get('seeding'))
        self.metrics.seed_pending_torrents.labels(self.instance_name).set(filtered_data.get('seed pending'))
        self.metrics.stopped_torrents.labels(self.instance_name).set(filtered_data.get('stopped'))
        
        self.metrics.transmission_data_processing_latency_seconds.labels(self.instance_name).observe(time.time() - start_data_processing_latency_time)
                                        

    def query_and_process_data(self) -> None:
        '''Run all query and process methods in the Transmission instance'''
        try:
            self.get_torrent_data()
        except Exception as e:
            raise MateyQueryAndProcessDataError(self.instance_name, e)

