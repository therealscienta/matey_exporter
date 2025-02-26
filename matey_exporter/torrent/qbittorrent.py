
import time
from prometheus_client import Gauge, Summary
import qbittorrentapi
from collections import defaultdict

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
        super().__init__(qbittorrentapi.Client(**{
                        'host': kwargs.get('host_url'), 
                        'username' : kwargs.get('username'), 
                        'password' : kwargs.get('password')}), **kwargs)
        self.api.VERIFY_WEBUI_CERTIFICATE = kwargs.get('verify')
        self.metrics = MateyQbittorrentPrometheusMetrics()

        
    def filter_data(self, data: dict) -> dict:
        '''
        Filter returned torrent data based on state of torrent. 
        Dictionary keys are based on states from official API documentation:
        https://github.com/qbittorrent/qBittorrent/wiki/WebUI-API-(qBittorrent-4.1)#get-torrent-list
        '''
        
        data_dict = defaultdict(int)
        for torrent in data: data_dict[torrent.state] += 1
        return data_dict


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
        filtered_data = self.filter_data(data)
        
        self.metrics.qbittorrent_torrents_error.labels(self.instance_name).set(filtered_data.get('error'))
        self.metrics.qbittorrent_torrents_missingFiles.labels(self.instance_name).set(filtered_data.get('missingFiles'))
        self.metrics.qbittorrent_torrents_allocating.labels(self.instance_name).set(filtered_data.get('allocating'))
        self.metrics.qbittorrent_torrents_checkingResumeData.labels(self.instance_name).set(filtered_data.get('checkingResumeData'))
        self.metrics.qbittorrent_torrents_moving.labels(self.instance_name).set(filtered_data.get('moving'))
        self.metrics.qbittorrent_torrents_metaDL.labels(self.instance_name).set(filtered_data.get('metaDL'))
        self.metrics.qbittorrent_torrents_unknown.labels(self.instance_name).set(filtered_data.get('unknown'))
        self.metrics.qbittorrent_torrents_uploading.labels(self.instance_name).set(filtered_data.get('uploading'))
        self.metrics.qbittorrent_torrents_downloading.labels(self.instance_name).set(filtered_data.get('downloading'))
        self.metrics.qbittorrent_torrents_stalledUP.labels(self.instance_name).set(filtered_data.get('stalledUP'))
        self.metrics.qbittorrent_torrents_stalledDL.labels(self.instance_name).set(filtered_data.get('stalledDL'))
        self.metrics.qbittorrent_torrents_checkingUP.labels(self.instance_name).set(filtered_data.get('checkingUP'))
        self.metrics.qbittorrent_torrents_checkingDL.labels(self.instance_name).set(filtered_data.get('checkingDL'))
        self.metrics.qbittorrent_torrents_forcedUP.labels(self.instance_name).set(filtered_data.get('forcedUP'))
        self.metrics.qbittorrent_torrents_forcedDL.labels(self.instance_name).set(filtered_data.get('forcedDL'))
        self.metrics.qbittorrent_torrents_pausedUP.labels(self.instance_name).set(filtered_data.get('pausedUP'))
        self.metrics.qbittorrent_torrents_pausedDL.labels(self.instance_name).set(filtered_data.get('pausedDL'))
        self.metrics.qbittorrent_torrents_queuedUP.labels(self.instance_name).set(filtered_data.get('queuedUP'))
        self.metrics.qbittorrent_torrents_queuedDL.labels(self.instance_name).set(filtered_data.get('queuedDL'))
        self.metrics.qbittorrent_torrents_stoppedUP.labels(self.instance_name).set(filtered_data.get('stoppedUP'))
        self.metrics.qbittorrent_torrents_stoppedDL.labels(self.instance_name).set(filtered_data.get('stoppedDL'))
        
        self.metrics.qbittorrent_data_processing_latency_seconds.labels(self.instance_name).observe(time.time() - start_data_processing_latency_time)
                                        
        

    def query_and_process_data(self) -> None:
        '''Run all query and process methods in the Qbittorrent instance'''
        try:
            self.get_torrent_data()
        except Exception as e:
            raise MateyQueryAndProcessDataError(self.instance_name, e)