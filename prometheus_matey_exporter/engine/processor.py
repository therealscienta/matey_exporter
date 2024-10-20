
from prometheus_client import Gauge
from abc import ABC, abstractmethod

import sys
from pprint import pp

class MateyDataProcessorBase(ABC):
    
    @abstractmethod
    def get_data(self):
        pass

class MateyDataProcessorSonarr(MateyDataProcessorBase):
    
    def get_data(self, source):
        data = source.api.get_series()
        data_missing = source.api.get_wanted()
        status = {'upcoming': 0, 'ended': 0, 'continuing': 0}
        monitored = 0
        missing_series = 0
        missing_episodes = len(data_missing)
        
        for d in data:
            status[d['status']] += 1
            if d['monitored'] == True : monitored += 1
            if d['status'] == 'upcoming' or d['statistics']['sizeOnDisk'] == 0: missing_series += 1

        source.sonarr_series_total.labels('sonarr', source.instance_name).set(len(data))
        source.sonarr_wanted_series_total.labels('sonarr', source.instance_name).set(missing_series)
        source.sonarr_wanted_episodes_total.labels('sonarr', source.instance_name).set(missing_episodes)
        source.sonarr_monitored_series_total.labels('sonarr', source.instance_name).set(monitored)
        source.sonarr_upcoming_series_total.labels('sonarr', source.instance_name).set(status['upcoming'])
        source.sonarr_ended_series_total.labels('sonarr', source.instance_name).set(status['ended'])
        source.sonarr_continuing_series_total.labels('sonarr', source.instance_name).set(status['continuing'])