from prometheus_matey_exporter.common.enums import MateyType
from prometheus_matey_exporter.common.processor import DataProcessorBase

from .base import StarrClass

import time
from pyarr import ReadarrAPI
from prometheus_client import Gauge, Summary

    
class Mateyreadarr(StarrClass):
    TYPE = MateyType.READARR
    
    def __init__(self, url, api_key, instance_name, verify=False):
        super().__init__(url, api_key, instance_name)
        self.api = ReadarrAPI(self.url, self.api_key)
        self.api.session.verify = verify
        # TODO
        
        self.readarr_movies_total =              Gauge('readarr_movies_total',            'Number of total movies',           labelnames=['instance'])
        self.readarr_wanted_movies_total =       Gauge('readarr_wanted_movies_total',     'Number of total missing movies',   labelnames=['instance'])
        self.readarr_wanted_episodes_total =     Gauge('readarr_wanted_episodes_total',   'Number of total missing episodes', labelnames=['instance'])
        self.readarr_episodes_in_queue_total =   Gauge('readarr_episodes_in_queue_total', 'Number of episodes in queue',      labelnames=['instance'])
        self.readarr_monitored_movies_total =    Gauge('readarr_monitored_movies_total',  'Number of Monitored movies',       labelnames=['instance'])
        self.readarr_upcoming_movies_total =     Gauge('readarr_upcoming_movies_total',   'Number of Upcoming movies',        labelnames=['instance'])
        self.readarr_ended_movies_total =        Gauge('readarr_ended_movies_total',      'Number of Ended movies',           labelnames=['instance'])
        self.readarr_continuing_movies_total =   Gauge('readarr_continuing_movies_total', 'Number of Continuing movies',      labelnames=['instance'])
        self.readarr_health_notifications =      Gauge('readarr_health_notifications',    'Number of Health notifications',   labelnames=['instance'])
        
        self.readarr_api_query_latency_seconds =         Summary('readarr_api_query_latency_seconds',       'Latency for a single API query',       labelnames=['instance'])
        self.readarr_data_processing_latency_seconds =   Summary('readarr_data_processing_latency_seconds', 'Latency for exporter data processing', labelnames=['instance'])
        
    def update(self):
        ReadarrDataProcessor.get_data(self)

class ReadarrDataProcessor(DataProcessorBase):
    
    def get_data(source):
        start_time = time.time()
        data = source.api.get_movies()
        source.readarr_api_query_latency_seconds.labels('readarr', source.instance_name).observe(time.time() - start_time) # Time first API request TODO
        
        episoded_wanted = len(source.api.get_wanted(page_size=9999)['records']) # TODO check if page_size can be something else
        episodes_qeued = len(source.api.get_queue(page_size=9999)['records'])
        health = len(source.api.get_health())
        status = {'upcoming': 0, 'ended': 0, 'continuing': 0}
        monitored = 0
        missing_movies = 0
        movies_total = len(data)
        
        for d in data:
            status[d['status']] += 1
            if d['monitored'] == True : monitored += 1
            if d['status'] == 'upcoming' or d['statistics']['sizeOnDisk'] == 0: missing_movies += 1

        source.readarr_data_processing_latency_seconds.labels(instance=source.instance_name).observe(time.time() - start_time) # Time data processing
        source.readarr_movies_total.labels(instance=source.instance_name).set(movies_total)
        source.readarr_wanted_movies_total.labels(instance=source.instance_name).set(missing_movies)
        source.readarr_wanted_episodes_total.labels(instance=source.instance_name).set(episoded_wanted)
        source.readarr_episodes_in_queue_total.labels(instance=source.instance_name).set(episodes_qeued)
        source.readarr_monitored_movies_total.labels(instance=source.instance_name).set(monitored)
        source.readarr_upcoming_movies_total.labels(instance=source.instance_name).set(status['upcoming'])
        source.readarr_ended_movies_total.labels(instance=source.instance_name).set(status['ended'])
        source.readarr_continuing_movies_total.labels(instance=source.instance_name).set(status['continuing'])
        source.readarr_health_notifications.labels(instance=source.instance_name).set(health)