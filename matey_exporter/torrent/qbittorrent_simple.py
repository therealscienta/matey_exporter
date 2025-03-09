
import time
from prometheus_client import Gauge, Summary
import qbittorrentapi
from collections import Counter

from matey_exporter.common.exceptions import MateyQueryAndProcessDataError
from matey_exporter.common.decorators import singleton
from matey_exporter.common.base import BaseMateyClass

@singleton        
class MateyQbittorrentPrometheusMetrics:
    def __init__(self):
        self.qbittorrent_torrents_error =           Gauge('qbittorrent_torrents_leeching',      'Number of leeching torrents',              labelnames=['instance'])
        self.qbittorrent_torrents_missingFiles =    Gauge('qbittorrent_torrents_missingFiles',  'Number of torrents with missing files',    labelnames=['instance'])
        self.qbittorrent_torrents_allocating =      Gauge('qbittorrent_torrents_allocating',    'Number of torrents allocating space',      labelnames=['instance'])
        self.qbittorrent_torrents_moving =          Gauge('qbittorrent_torrents_moving',        'Number of torrents moving',                labelnames=['instance'])
        self.qbittorrent_torrents_metaDL =          Gauge('qbittorrent_torrents_metaDL',        'Number of torrents downloading metadata',  labelnames=['instance'])
        self.qbittorrent_torrents_unknown =         Gauge('qbittorrent_torrents_unknown',       'Number of torrents in unknown state',      labelnames=['instance'])
        self.qbittorrent_torrents_uploading =       Gauge('qbittorrent_torrents_uploading',     'Number of uploading torrents',             labelnames=['instance'])
        self.qbittorrent_torrents_downloading =     Gauge('qbittorrent_torrents_downloading',   'Number of downloading torrents',           labelnames=['instance'])
        self.qbittorrent_torrents_stalledUP =       Gauge('qbittorrent_torrents_stalledUP',     'Number of stalledUP torrents',             labelnames=['instance'])
        self.qbittorrent_torrents_stalledDL =       Gauge('qbittorrent_torrents_stalledDL',     'Number of stalledDL torrents',             labelnames=['instance'])
        self.qbittorrent_torrents_checkingUP =      Gauge('qbittorrent_torrents_checkingUP',    'Number of checkingUP torrents',            labelnames=['instance'])
        self.qbittorrent_torrents_checkingDL =      Gauge('qbittorrent_torrents_checkingDL',    'Number of checkingDL torrents',            labelnames=['instance'])
        self.qbittorrent_torrents_forcedUP =        Gauge('qbittorrent_torrents_forcedUP',      'Number of forcedUP torrents',              labelnames=['instance'])
        self.qbittorrent_torrents_forcedDL =        Gauge('qbittorrent_torrents_forcedDL',      'Number of forcedDL torrents',              labelnames=['instance'])
        self.qbittorrent_torrents_pausedUP =        Gauge('qbittorrent_torrents_pausedUP',      'Number of pausedUP torrents',              labelnames=['instance'])
        self.qbittorrent_torrents_pausedDL =        Gauge('qbittorrent_torrents_pausedDL',      'Number of pausedDL torrents',              labelnames=['instance'])
        self.qbittorrent_torrents_queuedUP =        Gauge('qbittorrent_torrents_queuedUP',      'Number of queuedUP torrents',              labelnames=['instance'])
        self.qbittorrent_torrents_queuedDL =        Gauge('qbittorrent_torrents_queuedDL',      'Number of queuedDL torrents',              labelnames=['instance'])
        self.qbittorrent_torrents_stoppedUP =       Gauge('qbittorrent_torrents_stoppedUP',     'Number of stoppedUP torrents',             labelnames=['instance'])
        self.qbittorrent_torrents_stoppedDL =       Gauge('qbittorrent_torrents_stoppedDL',     'Number of stoppedDL torrents',             labelnames=['instance'])
        self.qbittorrent_torrents_checkingResumeData =  Gauge('qbittorrent_torrents_checkingResumeData',    'Number of torrents checking resume data',  labelnames=['instance'])

        
        self.qbittorrent_api_query_latency_seconds =         Summary('qbittorrent_api_query_latency_seconds',       'Latency for a single API query',       labelnames=['instance'])
        self.qbittorrent_data_processing_latency_seconds =   Summary('qbittorrent_data_processing_latency_seconds', 'Latency for exporter data processing', labelnames=['instance'])

    
class MateyQbittorrent(BaseMateyClass):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api = qbittorrentapi.Client(**{
            'host': kwargs.get('host_url'), 
            'username' : kwargs.get('username'), 
            'password' : kwargs.get('password')})
        self.api.VERIFY_WEBUI_CERTIFICATE = kwargs.get('verify')
        self.metrics = MateyQbittorrentPrometheusMetrics()

        
    def count_states(self, data: dict) -> dict:
        '''
        Count torrents by their state. 
        Dictionary keys are based on states from official API documentation:
        https://github.com/qbittorrent/qBittorrent/wiki/WebUI-API-(qBittorrent-4.1)#get-torrent-list
        '''
    
        counted_data = Counter()
        for torrent in data:
            counted_data[torrent.state] += 1
        return counted_data

    # TODO: Fix empty result handling!

    def get_torrent_data(self) -> None:
        '''
        Query qBittorrent API for torrent data and process results.
        '''
        
        self.api.auth_log_in()
        start_api_query_latency_time = time.time()
        data = self.api.torrents_info()
        self.metrics.qbittorrent_api_query_latency_seconds.labels(self.instance_name).observe(time.time() - start_api_query_latency_time)
        self.api.auth_log_out()
        
        start_data_processing_latency_time = time.time()
        data_counted_states = self.count_states(data)
        
        self.metrics.qbittorrent_torrents_error.labels(self.instance_name).set(data_counted_states.get('error', 0))
        self.metrics.qbittorrent_torrents_missingFiles.labels(self.instance_name).set(data_counted_states.get('missingFiles', 0))
        self.metrics.qbittorrent_torrents_allocating.labels(self.instance_name).set(data_counted_states.get('allocating', 0))
        self.metrics.qbittorrent_torrents_checkingResumeData.labels(self.instance_name).set(data_counted_states.get('checkingResumeData', 0))
        self.metrics.qbittorrent_torrents_moving.labels(self.instance_name).set(data_counted_states.get('moving', 0))
        self.metrics.qbittorrent_torrents_metaDL.labels(self.instance_name).set(data_counted_states.get('metaDL', 0))
        self.metrics.qbittorrent_torrents_unknown.labels(self.instance_name).set(data_counted_states.get('unknown', 0))
        self.metrics.qbittorrent_torrents_uploading.labels(self.instance_name).set(data_counted_states.get('uploading', 0))
        self.metrics.qbittorrent_torrents_downloading.labels(self.instance_name).set(data_counted_states.get('downloading', 0))
        self.metrics.qbittorrent_torrents_stalledUP.labels(self.instance_name).set(data_counted_states.get('stalledUP', 0))
        self.metrics.qbittorrent_torrents_stalledDL.labels(self.instance_name).set(data_counted_states.get('stalledDL', 0))
        self.metrics.qbittorrent_torrents_checkingUP.labels(self.instance_name).set(data_counted_states.get('checkingUP', 0))
        self.metrics.qbittorrent_torrents_checkingDL.labels(self.instance_name).set(data_counted_states.get('checkingDL', 0))
        self.metrics.qbittorrent_torrents_forcedUP.labels(self.instance_name).set(data_counted_states.get('forcedUP', 0))
        self.metrics.qbittorrent_torrents_forcedDL.labels(self.instance_name).set(data_counted_states.get('forcedDL', 0))
        self.metrics.qbittorrent_torrents_pausedUP.labels(self.instance_name).set(data_counted_states.get('pausedUP', 0))
        self.metrics.qbittorrent_torrents_pausedDL.labels(self.instance_name).set(data_counted_states.get('pausedDL', 0))
        self.metrics.qbittorrent_torrents_queuedUP.labels(self.instance_name).set(data_counted_states.get('queuedUP', 0))
        self.metrics.qbittorrent_torrents_queuedDL.labels(self.instance_name).set(data_counted_states.get('queuedDL', 0))
        self.metrics.qbittorrent_torrents_stoppedUP.labels(self.instance_name).set(data_counted_states.get('stoppedUP', 0))
        self.metrics.qbittorrent_torrents_stoppedDL.labels(self.instance_name).set(data_counted_states.get('stoppedDL', 0))

        self.metrics.qbittorrent_data_processing_latency_seconds.labels(self.instance_name).observe(time.time() - start_data_processing_latency_time)
                                        
        

    def query_and_process_data(self) -> None:
        '''Run all query and process methods in the Qbittorrent instance'''
        try:
            self.get_torrent_data()
        except Exception as e:
            raise MateyQueryAndProcessDataError(self.instance_name, e)