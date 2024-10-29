
from .base import BaseRadarrClass

import time
from pyarr import RadarrAPI
from prometheus_client import Gauge, Summary

    
class MateyRadarr(BaseRadarrClass):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.radarr_movies_total =              Gauge('radarr_movies_total',            'Number of total movies',           labelnames=['instance'])
        # self.radarr_wanted_movies_total =       Gauge('radarr_wanted_movies_total',     'Number of total missing movies',   labelnames=['instance'])
        # self.radarr_wanted_episodes_total =     Gauge('radarr_wanted_episodes_total',   'Number of total missing episodes', labelnames=['instance'])
        # self.radarr_episodes_in_queue_total =   Gauge('radarr_episodes_in_queue_total', 'Number of episodes in queue',      labelnames=['instance'])
        # self.radarr_monitored_movies_total =    Gauge('radarr_monitored_movies_total',  'Number of Monitored movies',       labelnames=['instance'])
        # self.radarr_upcoming_movies_total =     Gauge('radarr_upcoming_movies_total',   'Number of Upcoming movies',        labelnames=['instance'])
        # self.radarr_ended_movies_total =        Gauge('radarr_ended_movies_total',      'Number of Ended movies',           labelnames=['instance'])
        # self.radarr_continuing_movies_total =   Gauge('radarr_continuing_movies_total', 'Number of Continuing movies',      labelnames=['instance'])
        # self.radarr_health_notifications =      Gauge('radarr_health_notifications',    'Number of Health notifications',   labelnames=['instance'])
        
        self.radarr_api_query_latency_seconds =         Summary('radarr_api_query_latency_seconds',       'Latency for a single API query',       labelnames=['instance'])
        self.radarr_data_processing_latency_seconds =   Summary('radarr_data_processing_latency_seconds', 'Latency for exporter data processing', labelnames=['instance'])
        
    def update(self):
        start_time = time.time()
        data = self.api.get_movie()
        self.radarr_api_query_latency_seconds.labels(self.instance_name).observe(time.time() - start_time) # Time first API request TODO
        
        # episoded_wanted = len(self.api.get_wanted(page_size=9999)['records']) # TODO check if page_size can be something else
        # episodes_qeued = len(self.api.get_queue(page_size=9999)['records'])
        # health = len(self.api.get_health())
        # status = {'upcoming': 0, 'ended': 0, 'continuing': 0}
        # monitored = 0
        # missing_movies = 0
        movies_total = len(data)
        
        # for d in data:
        #     status[d['status']] += 1
        #     if d['monitored'] == True : monitored += 1
        #     if d['status'] == 'upcoming' or d['statistics']['sizeOnDisk'] == 0: missing_movies += 1

        self.radarr_data_processing_latency_seconds.labels(instance=self.instance_name).observe(time.time() - start_time) # Time data processing
        self.radarr_movies_total.labels(instance=self.instance_name).set(movies_total)
        # self.radarr_wanted_movies_total.labels(instance=self.instance_name).set(missing_movies)
        # self.radarr_wanted_episodes_total.labels(instance=self.instance_name).set(episoded_wanted)
        # self.radarr_episodes_in_queue_total.labels(instance=self.instance_name).set(episodes_qeued)
        # self.radarr_monitored_movies_total.labels(instance=self.instance_name).set(monitored)
        # self.radarr_upcoming_movies_total.labels(instance=self.instance_name).set(status['upcoming'])
        # self.radarr_ended_movies_total.labels(instance=self.instance_name).set(status['ended'])
        # self.radarr_continuing_movies_total.labels(instance=self.instance_name).set(status['continuing'])
        # self.radarr_health_notifications.labels(instance=self.instance_name).set(health)