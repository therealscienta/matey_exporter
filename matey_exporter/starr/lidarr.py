from .base import BaseStarrClass

import time
from prometheus_client import Gauge, Summary
from pyarr import LidarrAPI
    
class MateyRadarr(BaseStarrClass):
    
    def __init__(self, **kwargs):
        super().__init__(LidarrAPI, **kwargs)
        pass