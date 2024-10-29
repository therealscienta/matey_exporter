
from .base import BaseSonarrClass

import time
from prometheus_client import Gauge, Summary

    
class MateySonarr(BaseSonarrClass):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
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
        
    def update(self):
        start_time = time.time()
        data = self.api.get_series()
        self.sonarr_api_query_latency_seconds.labels(self.instance_name).observe(time.time() - start_time) # Time first API request TODO
        
        episoded_wanted = len(self.api.get_wanted(page_size=9999)['records']) # TODO check if page_size can be something else
        episodes_qeued = len(self.api.get_queue(page_size=9999)['records'])
        health = len(self.api.get_health())
        status = {'upcoming': 0, 'ended': 0, 'continuing': 0}
        monitored = 0
        missing_series = 0
        series_total = len(data)
        
        for d in data:
            status[d['status']] += 1
            if d['monitored'] == True : monitored += 1
            if d['status'] == 'upcoming' or d['statistics']['sizeOnDisk'] == 0: missing_series += 1

        self.sonarr_data_processing_latency_seconds.labels(instance=self.instance_name).observe(time.time() - start_time) # Time data processing
        self.sonarr_series_total.labels(instance=self.instance_name).set(series_total)
        self.sonarr_wanted_series_total.labels(instance=self.instance_name).set(missing_series)
        self.sonarr_wanted_episodes_total.labels(instance=self.instance_name).set(episoded_wanted)
        self.sonarr_episodes_in_queue_total.labels(instance=self.instance_name).set(episodes_qeued)
        self.sonarr_monitored_series_total.labels(instance=self.instance_name).set(monitored)
        self.sonarr_upcoming_series_total.labels(instance=self.instance_name).set(status['upcoming'])
        self.sonarr_ended_series_total.labels(instance=self.instance_name).set(status['ended'])
        self.sonarr_continuing_series_total.labels(instance=self.instance_name).set(status['continuing'])
        self.sonarr_health_notifications.labels(instance=self.instance_name).set(health)

