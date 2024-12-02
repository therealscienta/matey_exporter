
from prometheus_client import Gauge, Summary
from pyarr import SonarrAPI

from matey_exporter.common import MateyQueryAndProcessDataError, singleton
from .base import BaseStarrClass

@singleton
class MateySonarrPrometheusMetrics:
    def __init__(self):
        self.sonarr_series =                Gauge('sonarr_series',                  'Number of total series',           labelnames=['instance'])
        self.sonarr_wanted_series =         Gauge('sonarr_wanted_series',           'Number of total missing series',   labelnames=['instance'])
        self.sonarr_wanted_episodes =       Gauge('sonarr_wanted_episodes',         'Number of total missing episodes', labelnames=['instance'])
        self.sonarr_episodes_in_queue =     Gauge('sonarr_episodes_in_queue',       'Number of episodes in queue',      labelnames=['instance'])
        self.sonarr_monitored_series =      Gauge('sonarr_monitored_series',        'Number of Monitored series',       labelnames=['instance'])
        self.sonarr_upcoming_series =       Gauge('sonarr_upcoming_series',         'Number of Upcoming series',        labelnames=['instance'])
        self.sonarr_ended_series =          Gauge('sonarr_ended_series',            'Number of Ended series',           labelnames=['instance'])
        self.sonarr_continuing_series =     Gauge('sonarr_continuing_series',       'Number of Continuing series',      labelnames=['instance'])
        self.sonarr_health_notifications =  Gauge('sonarr_health_notifications',    'Number of Health notifications',   labelnames=['instance'])
        
        self.sonarr_api_query_latency_seconds =         Summary('sonarr_api_query_latency_seconds',       'Latency for a single API query',       labelnames=['instance'])
        self.sonarr_data_processing_latency_seconds =   Summary('sonarr_data_processing_latency_seconds', 'Latency for exporter data processing', labelnames=['instance'])

    
class MateySonarr(BaseStarrClass):
    
    def __init__(self, **kwargs):
        super().__init__(SonarrAPI, **kwargs)
        self.metrics = MateySonarrPrometheusMetrics()

        
    def get_series_data_task(self):
        data = self.api.get_series()
        monitored = 0
        missing_series = 0
        status = {'upcoming': 0, 'ended': 0, 'continuing': 0, 'deleted': 0}
        for d in data:
            status[d['status']] += 1
            if d['monitored'] == True : monitored += 1
            if d['status'] == 'upcoming' or d['statistics']['sizeOnDisk'] == 0: missing_series += 1
    
        self.metrics.sonarr_series.labels(instance=self.instance_name).set(len(data))
        self.metrics.sonarr_wanted_series.labels(instance=self.instance_name).set(missing_series)
        self.metrics.sonarr_monitored_series.labels(instance=self.instance_name).set(monitored)
        self.metrics.sonarr_continuing_series.labels(instance=self.instance_name).set(status.get('continuing'))
        self.metrics.sonarr_upcoming_series.labels(instance=self.instance_name).set(status.get('upcoming'))
        self.metrics.sonarr_ended_series.labels(instance=self.instance_name).set(status.get('ended'))
        
    def get_wanted_series_data_task(self):
        data = self.api.get_wanted(page_size=9999) # TODO: see if there's a way to not use page_size
        self.metrics.sonarr_wanted_series.labels(instance=self.instance_name).set(len(data['records']))
        
    def get_episodes_in_queue_data_task(self):
        data = self.api.get_queue(page_size=9999) # TODO: see if there's a way to not use page_size
        self.metrics.sonarr_episodes_in_queue.labels(instance=self.instance_name).set(len(data['records']))
        
    def get_health_data_task(self):
        data = self.api.get_health()
        self.metrics.sonarr_health_notifications.labels(instance=self.instance_name).set(len(data))
      
    def query_and_process_data(self):
        '''Run all query and process methods in the Sonarr instance'''
        try:
            self.get_series_data_task()
            self.get_wanted_series_data_task()
            self.get_episodes_in_queue_data_task()
            self.get_health_data_task()
        except Exception as e:
            raise MateyQueryAndProcessDataError(self.instance_name, e)


