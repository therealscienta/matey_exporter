
#from prometheus_matey_exporter.common.commons import arr_class
from prometheus_matey_exporter.common.commons import MateyType

from pyarr import SonarrAPI
from prometheus_client import Gauge, Summary

class arr_class:
    def __init__(self, host_url, api_key, instance_name):
        self.url = host_url
        self.api_key = api_key
        self.instance_name = instance_name
        self.api = None
    
class matey_sonarr(arr_class):
    TYPE = MateyType.SONARR
    
    def __init__(self, url, api_key, instance_name):
        super().__init__(url, api_key, instance_name)
        self.api = SonarrAPI(self.url, self.api_key)
        # TODO
        self.api.session.verify = False
        self.sonarr_series_total =              Gauge('sonarr_series_total',            'Number of total series',           labelnames=['instance', 'type'])
        self.sonarr_wanted_series_total =       Gauge('sonarr_wanted_series_total',     'Number of total missing series',   labelnames=['instance', 'type'])
        self.sonarr_wanted_episodes_total =     Gauge('sonarr_wanted_episodes_total',   'Number of total missing episodes', labelnames=['instance', 'type'])
        self.sonarr_episodes_in_queue_total =   Gauge('sonarr_episodes_in_queue_total', 'Number of episodes in queue',      labelnames=['instance', 'type'])
        self.sonarr_monitored_series_total =    Gauge('sonarr_monitored_series_total',  'Number of Monitored series',       labelnames=['instance', 'type'])
        self.sonarr_upcoming_series_total =     Gauge('sonarr_upcoming_series_total',   'Number of Upcoming series',        labelnames=['instance', 'type'])
        self.sonarr_ended_series_total =        Gauge('sonarr_ended_series_total',      'Number of Ended series',           labelnames=['instance', 'type'])
        self.sonarr_continuing_series_total =   Gauge('sonarr_continuing_series_total', 'Number of Continuing series',      labelnames=['instance', 'type'])
        self.sonarr_health_notifications =      Gauge('sonarr_health_notifications',    'Number of Health notifications',   labelnames=['instance', 'type'])
        
        self.sonarr_api_query_latency_seconds =         Summary('sonarr_api_query_latency_seconds',       'Latency for a single API query',       labelnames=['instance', 'type'])
        self.sonarr_data_processing_latency_seconds =   Summary('sonarr_data_processing_latency_seconds', 'Latency for exporter data processing', labelnames=['instance', 'type'])
        
        
    def get_series(self):
        return self.api.get_series()
    
