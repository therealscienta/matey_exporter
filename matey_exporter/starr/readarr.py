from .base import BaseStarrClass
from matey_exporter.common.enums import MateyType

import time
from prometheus_client import Gauge, Summary
from pyarr import ReadarrAPI
    
class MateyRadarr(BaseStarrClass):
    TYPE = MateyType.READARR
    
    def __init__(self, **kwargs):
        super().__init__(ReadarrAPI, **kwargs)
        pass