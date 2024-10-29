
from prometheus_matey_exporter.common.enums import MateyType
from prometheus_matey_exporter.common.processor import DataProcessorBase

from .base import StarrClass

import time
from pyarr import SonarrAPI
from prometheus_client import Gauge, Summary

    
class MateySonarr(StarrClass):
    TYPE = MateyType.SONARR
    
    def __init__(self, url, api_key, instance_name, verify=False):
        super().__init__(url, api_key, instance_name)
        self.api = SonarrAPI(self.url, self.api_key)
        self.api.session.verify = verify
        # TODO
        
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
        SonarrDataProcessor.get_data(self)

class SonarrDataProcessor(DataProcessorBase):
    
    def get_data(source):
        start_time = time.time()
        data = source.api.get_series()
        source.sonarr_api_query_latency_seconds.labels('sonarr', source.instance_name).observe(time.time() - start_time) # Time first API request TODO
        
        episoded_wanted = len(source.api.get_wanted(page_size=9999)['records']) # TODO check if page_size can be something else
        episodes_qeued = len(source.api.get_queue(page_size=9999)['records'])
        health = len(source.api.get_health())
        status = {'upcoming': 0, 'ended': 0, 'continuing': 0}
        monitored = 0
        missing_series = 0
        series_total = len(data)
        
        for d in data:
            status[d['status']] += 1
            if d['monitored'] == True : monitored += 1
            if d['status'] == 'upcoming' or d['statistics']['sizeOnDisk'] == 0: missing_series += 1

        source.sonarr_data_processing_latency_seconds.labels(instance=source.instance_name).observe(time.time() - start_time) # Time data processing
        source.sonarr_series_total.labels(instance=source.instance_name).set(series_total)
        source.sonarr_wanted_series_total.labels(instance=source.instance_name).set(missing_series)
        source.sonarr_wanted_episodes_total.labels(instance=source.instance_name).set(episoded_wanted)
        source.sonarr_episodes_in_queue_total.labels(instance=source.instance_name).set(episodes_qeued)
        source.sonarr_monitored_series_total.labels(instance=source.instance_name).set(monitored)
        source.sonarr_upcoming_series_total.labels(instance=source.instance_name).set(status['upcoming'])
        source.sonarr_ended_series_total.labels(instance=source.instance_name).set(status['ended'])
        source.sonarr_continuing_series_total.labels(instance=source.instance_name).set(status['continuing'])
        source.sonarr_health_notifications.labels(instance=source.instance_name).set(health)

    
