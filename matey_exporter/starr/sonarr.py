
from .base import BaseStarrClass
from matey_exporter.common import MateyType

import time
from prometheus_client import Gauge, Summary
from pyarr import SonarrAPI

class MateySonarrPrometheusMetrics:
    def __init__(self):
        self.sonarr_series_total =              Gauge('sonarr_series_total',            'Number of total series',           labelnames=['instance'])
        self.sonarr_wanted_series_total =       Gauge('sonarr_wanted_series_total',     'Number of total missing series',   labelnames=['instance'])
        self.sonarr_wanted_episodes_total =     Gauge('sonarr_wanted_episodes_total',   'Number of total missing episodes', labelnames=['instance'])
        self.sonarr_episodes_in_queue_total =   Gauge('sonarr_episodes_in_queue_total', 'Number of episodes in queue',      labelnames=['instance'])
        self.sonarr_monitored_series_total =    Gauge('sonarr_monitored_series_total',  'Number of Monitored series',       labelnames=['instance'])
        self.sonarr_upcoming_series_total =     Gauge('sonarr_upcoming_series_total',   'Number of Upcoming series',        labelnames=['instance'])
        self.sonarr_ended_series_total =        Gauge('sonarr_ended_series_total',      'Number of Ended series',           labelnames=['instance'])
        self.sonarr_continuing_series_total =   Gauge('sonarr_continuing_series_total', 'Number of Continuing series',      labelnames=['instance'])
        self.sonarr_health_notifications =      Gauge('sonarr_health_notifications',    'Number of Health notifications',   labelnames=['instance'])
        
        self.sonarr_api_query_latency_seconds =         Summary('sonarr_api_query_latency_seconds',       'Latency for a single API query',       labelnames=['instance'])
        self.sonarr_data_processing_latency_seconds =   Summary('sonarr_data_processing_latency_seconds', 'Latency for exporter data processing', labelnames=['instance'])
        

    
class MateySonarr(BaseStarrClass):
    TYPE = MateyType.SONARR
    
    def __init__(self, **kwargs):
        super().__init__(SonarrAPI, **kwargs)
        self.metrics = MateySonarrPrometheusMetrics()

        
    def get_series_data_task(self):
        data = self.api.get_series()
        monitored = 0
        missing_series = 0
        status = {'upcoming': 0, 'ended': 0, 'continuing': 0}
        for d in data:
            status[d['status']] += 1
            if d['monitored'] == True : monitored += 1
            if d['status'] == 'upcoming' or d['statistics']['sizeOnDisk'] == 0: missing_series += 1
    
        self.metrics.sonarr_series_total.labels(instance=self.instance_name).set(len(data))
        self.metrics.sonarr_wanted_series_total.labels(instance=self.instance_name).set(missing_series)
        self.metrics.sonarr_monitored_series_total.labels(instance=self.instance_name).set(monitored)
        self.metrics.sonarr_continuing_series_total.labels(instance=self.instance_name).set(status.get('continuing'))
        self.metrics.sonarr_upcoming_series_total.labels(instance=self.instance_name).set(status.get('upcoming'))
        self.metrics.sonarr_ended_series_total.labels(instance=self.instance_name).set(status.get('ended'))
        
    def get_wanted_series_data_task(self):
        data = self.api.get_wanted(page_size=9999) # TODO: see if there's a way to not use page_size
        self.metrics.sonarr_wanted_series_total.labels(instance=self.instance_name).set(len(data['records']))
        
    def get_episodes_in_queue_data_task(self):
        data = self.api.get_queue(page_size=9999) # TODO: see if there's a way to not use page_size
        self.metrics.sonarr_episodes_in_queue_total.labels(instance=self.instance_name).set(len(data['records']))
        
    def get_health_data_task(self):
        data = self.api.get_health()
        self.metrics.sonarr_health_notifications.labels(instance=self.instance_name).set(len(data))
        
    def query_and_process_data(self):
        '''Run all query and process methods in the Sonarr instance'''
        self.get_series_data_task()
        self.get_wanted_series_data_task()
        self.get_episodes_in_queue_data_task()
        self.get_health_data_task()


