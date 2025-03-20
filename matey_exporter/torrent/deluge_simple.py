
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
        self.allocating_torrents =    Gauge('allocating_torrents',  'Number of allocating torrents',    labelnames=['instance'])
        self.checking_torrents =      Gauge('checking_torrents',    'Number of checking torrents',      labelnames=['instance'])
        self.downloading_torrents =   Gauge('downloading_torrents', 'Number of downloading torrents',   labelnames=['instance'])
        self.moving_torrents =        Gauge('moving_torrents',      'Number of moving torrents',        labelnames=['instance'])
        self.seeding_torrents =       Gauge('seeding_torrents',     'Number of seeding torrents',       labelnames=['instance'])
        self.error_torrents =         Gauge('error_torrents',       'Number of errored torrents',       labelnames=['instance'])
        self.queued_torrents =        Gauge('queued_torrents',      'Number of queued torrents',        labelnames=['instance'])
        self.paused_torrents =        Gauge('paused_torrents',      'Number of paused torrents',        labelnames=['instance'])
        self.finished_torrents =      Gauge('finished_torrents',    'Number of finished torrents',      labelnames=['instance'])
        self.unfinished_torrents =    Gauge('unfinished_torrents',  'Number of stopped torrents',       labelnames=['instance'])
        
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
        self.metrics.allocating_torrents.labels(self.instance_name).set(data_counted_states.get('Checking metadata', 0))
        self.metrics.checking_torrents.labels(self.instance_name).set(data_counted_states.get('Downloading', 0))
        self.metrics.downloading_torrents.labels(self.instance_name).set(data_counted_states.get('Downloading', 0))
        self.metrics.moving_torrents.labels(self.instance_name).set(data_counted_states.get('Queued', 0))
        self.metrics.seeding_torrents.labels(self.instance_name).set(data_counted_states.get('Seeding', 0))
        self.metrics.error_torrents.labels(self.instance_name).set(data_counted_states.get('Seeding', 0))
        self.metrics.queued_torrents.labels(self.instance_name).set(data_counted_states.get('Paused', 0))
        self.metrics.paused_torrents.labels(self.instance_name).set(data_counted_states.get('Paused', 0))
        self.metrics.finished_torrents.labels(self.instance_name).set(data_counted_states.get('Finished', 0))
        self.metrics.unfinished_torrents.labels(self.instance_name).set(data_counted_states.get('Unfinished', 0))

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
