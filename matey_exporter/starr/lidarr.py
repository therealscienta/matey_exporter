from .base import BaseStarrClass
from matey_exporter.common.enums import MateyType

import time
from prometheus_client import Gauge, Summary
from pyarr import LidarrAPI
    
class MateyRadarr(BaseStarrClass):
    TYPE = MateyType.LIDARR
    
    def __init__(self, **kwargs):
        super().__init__(LidarrAPI, **kwargs)
        pass