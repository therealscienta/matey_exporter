
from prometheus_matey_exporter.common.enums import MateyType

from abc import ABC, abstractmethod


class BaseStarrClass(ABC):
    
    def __init__(self, **kwargs):
        self.host_url = kwargs['host_url']
        self.api_key = kwargs['api_key']
        self.instance_name = kwargs['instance_name']

    @abstractmethod
    def update(self):
        pass


class BaseSonarrClass(BaseStarrClass):
    TYPE = MateyType.SONARR
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from pyarr import SonarrAPI
        self.api = SonarrAPI(self.host_url, self.api_key)
        self.api.session.verify = kwargs['verify']


class BaseRadarrClass(BaseStarrClass):
    TYPE = MateyType.RADARR
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from pyarr import RadarrAPI
        self.api = RadarrAPI(self.host_url, self.api_key)
        self.api.session.verify = kwargs['verify']


class BaseLidarrClass(BaseStarrClass):
    TYPE = MateyType.LIDARR
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from pyarr import LidarrAPI
        self.api = LidarrAPI(self.host_url, self.api_key)
        self.api.session.verify = kwargs['verify']


class BaseReadarrClass(BaseStarrClass):
    TYPE = MateyType.READARR
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from pyarr import ReadarrAPI
        self.api = ReadarrAPI(self.host_url, self.api_key)
        self.api.session.verify = kwargs['verify']