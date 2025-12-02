
import time
from prometheus_client import Gauge, Summary
from transmission_rpc import Client
from collections import Counter

from matey_exporter.common.exceptions import MateyQueryAndProcessDataError 
from matey_exporter.common.decorators import singleton
from matey_exporter.common.base import BaseMateyClass

@singleton
class MateyTransmissionPrometheusMetricsSimple:
    def __init__(self):
        self.check_pending_torrents =       Gauge('check_pending_torrents',      'Number of check pending torrents',    labelnames=['instance'])
        self.checking_torrents =            Gauge('checking_torrents',           'Number of checking torrents',         labelnames=['instance'])
        self.downloading_torrents =         Gauge('downloading_torrents',        'Number of downloading torrents',      labelnames=['instance'])
        self.download_pending_torrents =    Gauge('download_pending_torrents',   'Number of download pending torrents', labelnames=['instance'])
        self.seeding_torrents =             Gauge('seeding_torrents',            'Number of seeding torrents',          labelnames=['instance'])
        self.seed_pending_torrents =        Gauge('seed_pending_torrents',       'Number of seed pending torrents',     labelnames=['instance'])
        self.stopped_torrents =             Gauge('stopped_torrents',            'Number of stopped torrents',          labelnames=['instance'])
        
        self.transmission_api_query_simple_latency_seconds =         Summary('transmission_api_query_simple_latency_seconds',       'Latency for a single API query',       labelnames=['instance'])
        self.transmission_simple_data_processing_latency_seconds =   Summary('transmission_simple_data_processing_latency_seconds', 'Latency for exporter data processing', labelnames=['instance'])

    
class MateyTransmissionSimple(BaseMateyClass):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api = Client(
            host=kwargs.get('host_url').replace('http://', ''), # TODO: Remove replace and fix URL parsing in config. Client does not want http://
            port=kwargs.get('port', 9091),
            username=kwargs.get('username'), 
            password=kwargs.get('password'))
        self.api._http_session.verify = self.verify
        self.metrics = MateyTransmissionPrometheusMetricsSimple()


    def count_states(self, data: dict) -> dict:
        '''
        Count torrents by their state. 
        Dictionary keys are based on states from official API documentation:
        https://transmission-rpc.readthedocs.io/en/v7.0.11/torrent.html#transmission_rpc.Torrent.status
        '''
        
        counted_data = Counter()
        for torrent in data:
            counted_data[torrent.get('status')] += 1
        return counted_data


    def get_torrent_data(self) -> None:
        '''
        Query Transmission API for torrent data and process results.
        '''

        start_api_query_latency_time = time.time()
        data = self.api.get_torrents()
        self.metrics.transmission_api_query_simple_latency_seconds.labels(self.instance_name).observe(time.time() - start_api_query_latency_time)
        
        start_data_processing_latency_time = time.time()
        data_counted_states = self.count_states(data)
        
        self.metrics.check_pending_torrents.labels(self.instance_name).set(data_counted_states.get('check pending', 0))
        self.metrics.checking_torrents.labels(self.instance_name).set(data_counted_states.get('checking', 0))
        self.metrics.downloading_torrents.labels(self.instance_name).set(data_counted_states.get('downloading', 0))
        self.metrics.download_pending_torrents.labels(self.instance_name).set(data_counted_states.get('download pending', 0))
        self.metrics.seeding_torrents.labels(self.instance_name).set(data_counted_states.get('seeding', 0))
        self.metrics.seed_pending_torrents.labels(self.instance_name).set(data_counted_states.get('seed pending', 0))
        self.metrics.stopped_torrents.labels(self.instance_name).set(data_counted_states.get('stopped', 0))
        
        self.metrics.transmission_simple_data_processing_latency_seconds.labels(self.instance_name).observe(time.time() - start_data_processing_latency_time)
                                        

    def query_and_process_data(self) -> None:
        '''Run all query and process methods in the Transmission instance'''
        try:
            self.get_torrent_data()
        except Exception as e:
            raise MateyQueryAndProcessDataError(self.instance_name, e)
