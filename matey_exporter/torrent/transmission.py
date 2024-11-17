
import time
from prometheus_client import Gauge, Summary
from transmission_rpc import Client

from .base import BaseTorrentClass

class MateyTransmissionPrometheusMetrics:
    def __init__(self):
        self.transmission_torrents_total =              Gauge('transmission_torrents_total',            'Number of total torrents',           labelnames=['instance'])
        # self.transmission_wanted_torrents_total =       Gauge('transmission_wanted_torrents_total',     'Number of total missing torrents',   labelnames=['instance'])
        # self.transmission_wanted_episodes_total =     Gauge('transmission_wanted_episodes_total',   'Number of total missing episodes', labelnames=['instance'])
        # self.transmission_episodes_in_queue_total =   Gauge('transmission_episodes_in_queue_total', 'Number of episodes in queue',      labelnames=['instance'])
        # self.transmission_monitored_torrents_total =    Gauge('transmission_monitored_torrents_total',  'Number of Monitored torrents',       labelnames=['instance'])
        # self.transmission_upcoming_torrents_total =     Gauge('transmission_upcoming_torrents_total',   'Number of Upcoming torrents',        labelnames=['instance'])
        # self.transmission_ended_torrents_total =        Gauge('transmission_ended_torrents_total',      'Number of Ended torrents',           labelnames=['instance'])
        # self.transmission_continuing_torrents_total =   Gauge('transmission_continuing_torrents_total', 'Number of Continuing torrents',      labelnames=['instance'])
        # self.transmission_health_notifications =      Gauge('transmission_health_notifications',    'Number of Health notifications',   labelnames=['instance'])
        
        self.transmission_api_query_latency_seconds =         Summary('transmission_api_query_latency_seconds',       'Latency for a single API query',       labelnames=['instance'])
        self.transmission_data_processing_latency_seconds =   Summary('transmission_data_processing_latency_seconds', 'Latency for exporter data processing', labelnames=['instance'])
    
class MateyTransmission(BaseTorrentClass):
    
    def __init__(self, **kwargs):
        super().__init__(Client(self.host_url, self.api_key), **kwargs)
        self.api._http_session = kwargs.get('verify') # TODO: Using private attribute
        self.metrics = MateyTransmissionPrometheusMetrics
        

        
    def update(self):
        start_time = time.time()
        data = self.api.get_torrents()
        self.transmission_api_query_latency_seconds.labels(self.instance_name).observe(time.time() - start_time) # Time first API request TODO
        
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

        self.transmission_data_processing_latency_seconds.labels(instance=self.instance_name).observe(time.time() - start_time) # Time data processing
        self.transmission_torrents_total.labels(instance=self.instance_name).set(torrents_total)
        # self.transmission_wanted_torrents_total.labels(instance=self.instance_name).set(missing_torrents)
        # self.transmission_wanted_episodes_total.labels(instance=self.instance_name).set(episoded_wanted)
        # self.transmission_episodes_in_queue_total.labels(instance=self.instance_name).set(episodes_qeued)
        # self.transmission_monitored_torrents_total.labels(instance=self.instance_name).set(monitored)
        # self.transmission_upcoming_torrents_total.labels(instance=self.instance_name).set(status['upcoming'])
        # self.transmission_ended_torrents_total.labels(instance=self.instance_name).set(status['ended'])
        # self.transmission_continuing_torrents_total.labels(instance=self.instance_name).set(status['continuing'])
        # self.transmission_health_notifications.labels(instance=self.instance_name).set(health)

