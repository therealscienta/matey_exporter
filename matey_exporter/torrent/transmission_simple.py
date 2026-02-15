
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
        self.transmission_torrents_check_pending =      Gauge('transmission_torrents_check_pending',      'Number of check pending torrents',    labelnames=['instance'])
        self.transmission_torrents_checking =           Gauge('transmission_torrents_checking',           'Number of checking torrents',         labelnames=['instance'])
        self.transmission_torrents_downloading =        Gauge('transmission_torrents_downloading',        'Number of downloading torrents',      labelnames=['instance'])
        self.transmission_torrents_download_pending =   Gauge('transmission_torrents_download_pending',   'Number of download pending torrents', labelnames=['instance'])
        self.transmission_torrents_seeding =            Gauge('transmission_torrents_seeding',            'Number of seeding torrents',          labelnames=['instance'])
        self.transmission_torrents_seed_pending =       Gauge('transmission_torrents_seed_pending',       'Number of seed pending torrents',     labelnames=['instance'])
        self.transmission_torrents_stopped =            Gauge('transmission_torrents_stopped',            'Number of stopped torrents',          labelnames=['instance'])
        
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
        
        self.metrics.transmission_torrents_check_pending.labels(self.instance_name).set(data_counted_states.get('check pending', 0))
        self.metrics.transmission_torrents_checking.labels(self.instance_name).set(data_counted_states.get('checking', 0))
        self.metrics.transmission_torrents_downloading.labels(self.instance_name).set(data_counted_states.get('downloading', 0))
        self.metrics.transmission_torrents_download_pending.labels(self.instance_name).set(data_counted_states.get('download pending', 0))
        self.metrics.transmission_torrents_seeding.labels(self.instance_name).set(data_counted_states.get('seeding', 0))
        self.metrics.transmission_torrents_seed_pending.labels(self.instance_name).set(data_counted_states.get('seed pending', 0))
        self.metrics.transmission_torrents_stopped.labels(self.instance_name).set(data_counted_states.get('stopped', 0))
        
        self.metrics.transmission_simple_data_processing_latency_seconds.labels(self.instance_name).observe(time.time() - start_data_processing_latency_time)
                                        

    def query_and_process_data(self) -> None:
        '''Run all query and process methods in the Transmission instance'''
        try:
            self.get_torrent_data()
        except Exception as e:
            raise MateyQueryAndProcessDataError(self.instance_name, e)
