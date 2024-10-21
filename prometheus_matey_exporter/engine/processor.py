
from abc import ABC, abstractmethod

import time

class MateyDataProcessorBase(ABC):
    
    @abstractmethod
    def get_data(self):
        raise(f'{self.__class__.__name__} class has not implemented function get_data.')

class MateyDataProcessorSonarr(MateyDataProcessorBase):
    
    def get_data(self, source):
        start_time = time.time()
        data = source.api.get_series()
        source.sonarr_api_query_latency_seconds.labels('sonarr', source.instance_name).observe(time.time() - start_time) # Time first API request
        
        episoded_wanted = len(source.api.get_wanted(page_size=9999)['records'])
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

        source.sonarr_data_processing_latency_seconds.labels('sonarr', source.instance_name).observe(time.time() - start_time) # Time data processing
        source.sonarr_series_total.labels('sonarr', source.instance_name).set(series_total)
        source.sonarr_wanted_series_total.labels('sonarr', source.instance_name).set(missing_series)
        source.sonarr_wanted_episodes_total.labels('sonarr', source.instance_name).set(episoded_wanted)
        source.sonarr_episodes_in_queue_total.labels('sonarr', source.instance_name).set(episodes_qeued)
        source.sonarr_monitored_series_total.labels('sonarr', source.instance_name).set(monitored)
        source.sonarr_upcoming_series_total.labels('sonarr', source.instance_name).set(status['upcoming'])
        source.sonarr_ended_series_total.labels('sonarr', source.instance_name).set(status['ended'])
        source.sonarr_continuing_series_total.labels('sonarr', source.instance_name).set(status['continuing'])
        source.sonarr_health_notifications.labels('sonarr', source.instance_name).set(health)
        