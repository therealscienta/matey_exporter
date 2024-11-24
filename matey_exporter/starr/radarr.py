
import time
from prometheus_client import Gauge, Summary
from pyarr import RadarrAPI

from matey_exporter.common import MateyQueryAndProcessDataError
from .base import BaseStarrClass

class MateyRadarrPrometheusMetrics:
    def __init__(self):
        self.radarr_movies =                    Gauge('radarr_movies',                      'Number of total movies',           labelnames=['instance'])
        self.radarr_missing_movies =            Gauge('radarr_missing_movies',              'Number of total missing movies',   labelnames=['instance'])
        self.radarr_monitored_movies =          Gauge('radarr_monitored_movies',            'Number of Monitored movies',       labelnames=['instance'])
        self.radarr_movies_in_queue =           Gauge('radarr_movies_in_queue',             'Number of movies in queue',        labelnames=['instance'])
        self.radarr_health_errors =             Gauge('radarr_health_errors',               'Radarr health errors',             labelnames=['instance'])
        self.radarr_health_warnings =           Gauge('radarr_health_warnings',             'Radarr health warnings',           labelnames=['instance'])
        self.radarr_health_ok =                 Gauge('radarr_health_ok',                   'Radarr health unknown Errors',     labelnames=['instance'])
        self.radarr_health_notice =             Gauge('radarr_health_unknownWarnings',      'Radarr unkown warnings',           labelnames=['instance'])
        self.radarr_queue_errors_bool =         Gauge('radarr_queue_errors_bool',           'Queue errors bool',                labelnames=['instance'])
        self.radarr_queue_warnings_bool =       Gauge('radarr_queue_warnings_bool',         'Queue warnings bool',              labelnames=['instance'])
        self.radarr_queue_unknownerrors_bool =  Gauge('radarr_queue_unknownerrors_bool',    'Queue unknown errors bool',        labelnames=['instance'])
        self.radarr_queue_unknownwarnings_bool= Gauge('radarr_queue_unknownwarnings_bool',  'Queue unknown warnings bool',      labelnames=['instance'])
        
        self.radarr_get_movie_api_query_latency_seconds =   Summary('radarr_get_movie_api_query_latency_seconds', 'Latency for a single API query',       labelnames=['instance'])
        self.radarr_data_processing_latency_seconds =       Summary('radarr_data_processing_latency_seconds',     'Latency for exporter data processing', labelnames=['instance'])
        

class MateyRadarr(BaseStarrClass):
    
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
            # TODO: Add d.get('genres') and/or d.get('released')? 

        self.metrics.radarr_movies.labels(instance=self.instance_name).set(len(data)) 
        self.metrics.radarr_missing_movies.labels(instance=self.instance_name).set(missing)
        self.metrics.radarr_monitored_movies.labels(instance=self.instance_name).set(monitored)
    

    def get_queue_data_task(self):
        data = self.api.get_queue()['records']
        self.metrics.radarr_movies_in_queue.labels(instance=self.instance_name).set(len(data))
    
   
    def get_queue_status_data_task(self):
        def bool_convert(bool_value):
            return {True: 1, False: 0}.get(bool_value)
        
        data = self.api.get_queue_status()
        self.metrics.radarr_movies_in_queue.labels(instance=self.instance_name).set(data.get('totalCount'))
        self.metrics.radarr_queue_errors_bool.labels(instance=self.instance_name).set(bool_convert(data.get('errors')))
        self.metrics.radarr_queue_warnings_bool.labels(instance=self.instance_name).set(bool_convert(data.get('warnings')))
        self.metrics.radarr_queue_unknownerrors_bool.labels(instance=self.instance_name).set(bool_convert(data.get('unknownErrors')))
        self.metrics.radarr_queue_unknownwarnings_bool.labels(instance=self.instance_name).set(bool_convert(data.get('unknownWarnings')))
    
   
    def get_health_data_task(self):
        health = {'warning': 0, 'error': 0, 'ok': 0, 'notice': 0}
        data = self.api.get_health()
        for d in data: health[d.get('type')] +=1
        
        self.metrics.radarr_health_errors.labels(instance=self.instance_name).set(health.get('error'))
        self.metrics.radarr_health_warnings.labels(instance=self.instance_name).set(health.get('warning'))
        self.metrics.radarr_health_ok.labels(instance=self.instance_name).set(health.get('ok'))
        self.metrics.radarr_health_notice.labels(instance=self.instance_name).set(health.get('notice'))
    

    def query_and_process_data(self):
        '''Run all query and process methods in the Radarr instance'''

        try:
            self.get_movie_data_task()
            self.get_queue_data_task()
            self.get_queue_status_data_task()
            self.get_health_data_task()
        except Exception as e:
            raise MateyQueryAndProcessDataError(self.instance_name, e)
