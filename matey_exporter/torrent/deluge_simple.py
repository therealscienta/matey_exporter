
import time
from collections import Counter
from prometheus_client import Gauge, Summary
from deluge_web_client import DelugeWebClient

from matey_exporter.common.base import BaseMateyClass
from matey_exporter.common.exceptions import MateyQueryAndProcessDataError
from matey_exporter.common.decorators import singleton


@singleton
class MateyDelugePrometheusMetricsSimple:
    def __init__(self):
        self.deluge_torrents_allocating =   Gauge('deluge_torrents_allocating',  'Number of allocating torrents',    labelnames=['instance'])
        self.deluge_torrents_checking =     Gauge('deluge_torrents_checking',    'Number of checking torrents',      labelnames=['instance'])
        self.deluge_torrents_downloading =  Gauge('deluge_torrents_downloading', 'Number of downloading torrents',   labelnames=['instance'])
        self.deluge_torrents_moving =       Gauge('deluge_torrents_moving',      'Number of moving torrents',        labelnames=['instance'])
        self.deluge_torrents_seeding =      Gauge('deluge_torrents_seeding',     'Number of seeding torrents',       labelnames=['instance'])
        self.deluge_torrents_error =        Gauge('deluge_torrents_error',       'Number of errored torrents',       labelnames=['instance'])
        self.deluge_torrents_queued =       Gauge('deluge_torrents_queued',      'Number of queued torrents',        labelnames=['instance'])
        self.deluge_torrents_paused =       Gauge('deluge_torrents_paused',      'Number of paused torrents',        labelnames=['instance'])
        self.deluge_torrents_finished =     Gauge('deluge_torrents_finished',    'Number of finished torrents',      labelnames=['instance'])
        self.deluge_torrents_unfinished =   Gauge('deluge_torrents_unfinished',  'Number of stopped torrents',       labelnames=['instance'])
        
        self.deluge_api_query_simple_latency_seconds = Summary(
            'deluge_api_query_simple_latency_seconds',
            'Latency for a single API query',       
            labelnames=['instance'])
        self.deluge_simple_data_processing_latency_seconds = Summary(
            'deluge_simple_data_processing_latency_seconds', 
            'Latency for exporter data processing', 
            labelnames=['instance'])


class MateyDelugeSimple(BaseMateyClass):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.host_url = kwargs.get('host_url')
        self.password = kwargs.get('password')
        self.instance_name = kwargs.get('instance_name')
        self.api = DelugeWebClient(url=self.host_url, password=self.password)
        self.metrics = MateyDelugePrometheusMetricsSimple()

    def count_states(self, data: dict) -> dict:
        '''
        Count torrents by their state.
        Dictionary keys are based on states from official Deluge API documentation.
        '''
        counted_data = Counter()
        for torrent_id, torrent_data in data.items():
            state = torrent_data.get('state')
            if state:
                counted_data[state] += 1
        return counted_data

    def get_torrent_data(self) -> None:
        '''
        Query Deluge API for torrent data and process results.
        '''
        start_api_query_latency_time = time.time()
        with self.api as client:
            api_data = client.get_torrents_status().result
        
        self.metrics.deluge_api_query_simple_latency_seconds.labels(
            self.instance_name).observe(time.time() - start_api_query_latency_time)

        start_data_processing_latency_time = time.time()
        data_counted_states = self.count_states(api_data)

        # Update the Prometheus metrics for various torrent states
        self.metrics.deluge_torrents_allocating.labels(self.instance_name).set(data_counted_states.get('Checking metadata', 0))
        self.metrics.deluge_torrents_checking.labels(self.instance_name).set(data_counted_states.get('Downloading', 0))
        self.metrics.deluge_torrents_downloading.labels(self.instance_name).set(data_counted_states.get('Downloading', 0))
        self.metrics.deluge_torrents_moving.labels(self.instance_name).set(data_counted_states.get('Queued', 0))
        self.metrics.deluge_torrents_seeding.labels(self.instance_name).set(data_counted_states.get('Seeding', 0))
        self.metrics.deluge_torrents_error.labels(self.instance_name).set(data_counted_states.get('Seeding', 0))
        self.metrics.deluge_torrents_queued.labels(self.instance_name).set(data_counted_states.get('Paused', 0))
        self.metrics.deluge_torrents_paused.labels(self.instance_name).set(data_counted_states.get('Paused', 0))
        self.metrics.deluge_torrents_finished.labels(self.instance_name).set(data_counted_states.get('Finished', 0))
        self.metrics.deluge_torrents_unfinished.labels(self.instance_name).set(data_counted_states.get('Unfinished', 0))

        self.metrics.deluge_simple_data_processing_latency_seconds.labels(
            self.instance_name).observe(time.time() - start_data_processing_latency_time)
                                        

    def query_and_process_data(self) -> None:
        '''
        Run all query and process methods in the deluge instance
        '''
        
        try:
            self.get_torrent_data()
        except Exception as e:
            raise MateyQueryAndProcessDataError(self.instance_name, e)
