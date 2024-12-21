
import time
from prometheus_client import Gauge, Summary, Enum
from deluge_web_client import DelugeWebClient

from matey_exporter.common import BaseMateyClass, MateyQueryAndProcessDataError, singleton

STATES = ['Checking',
          'Downloading',
          'Seeding',
          'Allocating',
          'Error',
          'Moving',
          'Queued',
          'Paused',
          'Finished',
          'Unfinished']

@singleton        
class MateyDelugePrometheusMetrics:
    
    def __init__(self):
        self.deluge_torrents_finished = Gauge(
            name='deluge_torrents_finished',
            documentation='Number of torrents with missing files',
            labelnames=['instance', 'torrent_name'])
        
        self.deluge_torrent_size_bytes = Gauge(
            name='deluge_torrent_size_bytes',
            documentation='Torrent total size in bytes',
            labelnames=['instance', 'torrent_name'])
        
        self.deluge_torrent_files = Gauge(
            name='deluge_torrent_files', 
            documentation='Number of Torrent files', 
            labelnames=['instance', 'torrent_name'])
        
        self.deluge_torrent_state = Enum(
            name='deluge_torrent_state', 
            documentation='Available Torrent states', 
            labelnames=['instance', 'torrent_name'],
            states=STATES)

        self.deluge_host_errors = Gauge(
            name='deluge_host_errors',
            documentation='Number of errors',
            labelnames=['instance'])
        
        self.deluge_api_query_latency_seconds = Summary(
            name='deluge_api_query_latency_seconds',
            documentation='Latency for a single API query',
            labelnames=['instance'])
        
        self.deluge_data_processing_latency_seconds =   Summary(
            name='deluge_data_processing_latency_seconds',
            documentation='Latency for exporter data processing',
            labelnames=['instance'])

    
class MateyDeluge(BaseMateyClass):
    
    def __init__(self, **kwargs):
        self.host_url = kwargs.get('host_url')
        self.password = kwargs.get('password')
        self.instance_name = kwargs.get('instance_name')
        self.api = DelugeWebClient(url=self.host_url, password=self.password)
        self.metrics = MateyDelugePrometheusMetrics()


    def get_torrent_data(self) -> None:
        '''
        Query Deluge API for torrent data and process results.
        '''

        start_api_query_latency_time = time.time()
        with self.api as client:
            data = client.get_torrents_status().result
        self.metrics.deluge_api_query_latency_seconds.labels(
            self.instance_name).observe(
                time.time() - start_api_query_latency_time)

        start_data_processing_latency_time = time.time()
        for t in data:

            self.metrics.deluge_torrents_finished.labels(
                instance=self.instance_name,
                torrent_name=data.get(t)['name']).set(
                    int(data.get(t).get('is_finished')))
                                                         
            self.metrics.deluge_torrent_size_bytes.labels(
                instance=self.instance_name,
                torrent_name=data.get(t)['name']).set(
                    data.get(t)['total_size'])
                                                          
            self.metrics.deluge_torrent_files.labels(
                instance=self.instance_name,
                torrent_name=data.get(t)['name']).set(
                    data.get(t)['num_files'])
                                                     
            self.metrics.deluge_torrent_state.labels(
                instance=self.instance_name,
                torrent_name=data.get(t)['name']).state(
                    data.get(t)['state'])
        
        self.metrics.deluge_data_processing_latency_seconds.labels(
            self.instance_name).observe(
                time.time() - start_data_processing_latency_time)
        
        
    def get_host_state(self):
        '''
        Query Deluge API for host state and process results.
        '''
        
        with self.api as client:
            error = client.get_host_status(client.get_hosts().id).error
        
        if error == None:
            error = 0
        else:
            error = 1
        self.metrics.deluge_host_errors.labels(instance=self.instance_name).set(error)
                                        
        

    def query_and_process_data(self) -> None:
        '''Run all query and process methods in the deluge instance'''
        try:
            self.get_torrent_data()
            self.get_host_state()
        except Exception as e:
            raise MateyQueryAndProcessDataError(self.instance_name, e)