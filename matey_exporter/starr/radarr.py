
from .base import BaseStarrClass
from matey_exporter.common import MateyType

import time
from prometheus_client import Gauge, Summary
from pyarr import RadarrAPI

class MateyRadarrPrometheusMetrics:
    def __init__(self):
        self.radarr_movies_total =              Gauge('radarr_movies_total',            'Number of total movies',           labelnames=['instance'])
        self.radarr_missing_movies_total =      Gauge('radarr_missing_movies_total',    'Number of total missing movies',   labelnames=['instance'])
        self.radarr_monitored_movies_total =    Gauge('radarr_monitored_movies_total',  'Number of Monitored movies',       labelnames=['instance'])
        
        # self.radarr_wanted_episodes_total =     Gauge('radarr_wanted_episodes_total',   'Number of total missing episodes', labelnames=['instance'])
        self.radarr_movies_in_queue_total =     Gauge('radarr_movies_in_queue_total',   'Number of movies in queue',        labelnames=['instance'])
        
        # self.radarr_upcoming_movies_total =     Gauge('radarr_upcoming_movies_total',   'Number of Upcoming movies',        labelnames=['instance'])
        # self.radarr_ended_movies_total =        Gauge('radarr_ended_movies_total',      'Number of Ended movies',           labelnames=['instance'])
        # self.radarr_continuing_movies_total =   Gauge('radarr_continuing_movies_total', 'Number of Continuing movies',      labelnames=['instance'])
        # self.radarr_health_notifications =      Gauge('radarr_health_notifications',    'Number of Health notifications',   labelnames=['instance'])
        
        self.radarr_health_errors_total =       Gauge('radarr_health_errors',             'Radarr health errors',             labelnames=['instance'])
        self.radarr_health_warnings_total =     Gauge('radarr_health_warnings',           'Radarr health warnings',           labelnames=['instance'])
        self.radarr_health_ok_total =           Gauge('radarr_health_ok',                 'Radarr health unknown Errors',     labelnames=['instance'])
        self.radarr_health_notice_total =       Gauge('radarr_health_unknownWarnings',    'Radarr unkown warnings',           labelnames=['instance'])
        
        #{'totalCount': 0, 'count': 0, 'unknownCount': 0, 'errors': False, 'warnings': False, 'unknownErrors': False, 'unknownWarnings': False}
        
        self.radarr_get_movie_api_query_latency_seconds =   Summary('radarr_get_movie_api_query_latency_seconds', 'Latency for a single API query', labelnames=['instance'])
        self.radarr_data_processing_latency_seconds =   Summary('radarr_data_processing_latency_seconds', 'Latency for exporter data processing', labelnames=['instance'])
        

class MateyRadarr(BaseStarrClass):
    TYPE = MateyType.RADARR
    
    def __init__(self, **kwargs):
        super().__init__(RadarrAPI, **kwargs)
        self.metrics = MateyRadarrPrometheusMetrics()
    
    def get_movie_data_task(self):
        
        start_time = time.time()
        data = self.api.get_movie()
        self.metrics.radarr_get_movie_api_query_latency_seconds.labels(self.instance_name).observe(time.time() - start_time)
        
        monitored = 0
        missing = 0
        
        for d in data:
            if d.get('monitored'): monitored += 1
            if not d.get('hasFile'): missing += 1
            # Add d.get('genres') and/or d.get('released')? TODO

        self.metrics.radarr_movies_total.labels(instance=self.instance_name).set(len(data)) 
        self.metrics.radarr_missing_movies_total.labels(instance=self.instance_name).set(missing)
        self.metrics.radarr_monitored_movies_total.labels(instance=self.instance_name).set(monitored)
    
    def get_queue_data_task(self):
        data = self.api.get_queue()['records']
        self.metrics.radarr_movies_in_queue_total.labels(instance=self.instance_name).set(len(data))
        
    def get_queue_details_data_task(self):
        data = self.api.get_queue_details()
        
    def get_queue_status_data_task(self):
        data = self.api.get_queue_status()
        
    def get_health_data_task(self):
        health = {'warning': 0, 'error': 0, 'ok': 0, 'notice': 0}
        data = self.api.get_health()
        for d in data: health[d.get('type')] +=1
        
        self.metrics.radarr_health_errors_total.labels(instance=self.instance_name).set(health.get('error'))
        self.metrics.radarr_health_warnings_total.labels(instance=self.instance_name).set(health.get('warning'))
        self.metrics.radarr_health_ok_total.labels(instance=self.instance_name).set(health.get('ok'))
        self.metrics.radarr_health_notice_total.labels(instance=self.instance_name).set(health.get('notice'))
    
    def query_and_process_data(self):
        '''Run all query and process methods in the Radarr instance'''
        self.get_movie_data_task()
        self.get_queue_data_task()
        self.get_health_data_task()