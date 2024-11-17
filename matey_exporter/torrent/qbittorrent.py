
import time
from prometheus_client import Gauge, Summary
from qbittorrent import Client

from .base import BaseTorrentClass
        
class MateyQbittorrentPrometheusMetrics:
    def __init__(self):
        self.qbittorrent_torrents_total =              Gauge('qbittorrent_torrents_total',            'Number of total torrents',           labelnames=['instance'])
        # self.qbittorrent_wanted_torrents_total =       Gauge('qbittorrent_wanted_torrents_total',     'Number of total missing torrents',   labelnames=['instance'])
        # self.qbittorrent_wanted_episodes_total =     Gauge('qbittorrent_wanted_episodes_total',   'Number of total missing episodes', labelnames=['instance'])
        # self.qbittorrent_episodes_in_queue_total =   Gauge('qbittorrent_episodes_in_queue_total', 'Number of episodes in queue',      labelnames=['instance'])
        # self.qbittorrent_monitored_torrents_total =    Gauge('qbittorrent_monitored_torrents_total',  'Number of Monitored torrents',       labelnames=['instance'])
        # self.qbittorrent_upcoming_torrents_total =     Gauge('qbittorrent_upcoming_torrents_total',   'Number of Upcoming torrents',        labelnames=['instance'])
        # self.qbittorrent_ended_torrents_total =        Gauge('qbittorrent_ended_torrents_total',      'Number of Ended torrents',           labelnames=['instance'])
        # self.qbittorrent_continuing_torrents_total =   Gauge('qbittorrent_continuing_torrents_total', 'Number of Continuing torrents',      labelnames=['instance'])
        # self.qbittorrent_health_notifications =      Gauge('qbittorrent_health_notifications',    'Number of Health notifications',   labelnames=['instance'])
        
        self.qbittorrent_api_query_latency_seconds =         Summary('qbittorrent_api_query_latency_seconds',       'Latency for a single API query',       labelnames=['instance'])
        self.qbittorrent_data_processing_latency_seconds =   Summary('qbittorrent_data_processing_latency_seconds', 'Latency for exporter data processing', labelnames=['instance'])

    
class MateyQbittorrent(BaseTorrentClass):
    
    def __init__(self, **kwargs):
        super().__init__(Client(self.host_url, self.api_key, verify=kwargs.get('verify')), **kwargs)
        self.api.login(kwargs.get('username'), self.api_key)
        self.metrics = MateyQbittorrentPrometheusMetrics()
        
    def get_update_tasks(self):
        '''Get all update tasks to run for the Sonarr instance'''
        yield self.get_series_data_task
        yield self.get_wanted_series_data_task
        yield self.get_episodes_in_queue_data_task
        yield self.get_health_data_task
        
    def update(self):
        start_time = time.time()
        data = self.api.torrents()
        self.qbittorrent_api_query_latency_seconds.labels(self.instance_name).observe(time.time() - start_time) # Time first API request TODO
        
        # episoded_wanted = len(self.api.get_wanted(page_size=9999)['records']) # TODO check if page_size can be something else
        # episodes_qeued = len(self.api.get_queue(page_size=9999)['records'])
        # health = len(self.api.get_health())
        # status = {'upcoming': 0, 'ended': 0, 'continuing': 0}
        # monitored = 0
        # missing_torrents = 0
        torrents_total = len(data)
        
        # for d in data:
        #     status[d['status']] += 1
        #     if d['monitored'] == True : monitored += 1
        #     if d['status'] == 'upcoming' or d['statistics']['sizeOnDisk'] == 0: missing_torrents += 1

        self.qbittorrent_data_processing_latency_seconds.labels(instance=self.instance_name).observe(time.time() - start_time) # Time data processing
        self.qbittorrent_torrents_total.labels(instance=self.instance_name).set(torrents_total)
        # self.qbittorrent_wanted_torrents_total.labels(instance=self.instance_name).set(missing_torrents)
        # self.qbittorrent_wanted_episodes_total.labels(instance=self.instance_name).set(episoded_wanted)
        # self.qbittorrent_episodes_in_queue_total.labels(instance=self.instance_name).set(episodes_qeued)
        # self.qbittorrent_monitored_torrents_total.labels(instance=self.instance_name).set(monitored)
        # self.qbittorrent_upcoming_torrents_total.labels(instance=self.instance_name).set(status['upcoming'])
        # self.qbittorrent_ended_torrents_total.labels(instance=self.instance_name).set(status['ended'])
        # self.qbittorrent_continuing_torrents_total.labels(instance=self.instance_name).set(status['continuing'])
        # self.qbittorrent_health_notifications.labels(instance=self.instance_name).set(health)

