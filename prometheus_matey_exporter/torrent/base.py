
from prometheus_matey_exporter.common.enums import MateyType
from abc import ABC, abstractmethod


class BaseTorrentClass(ABC):
    
    def __init__(self, **kwargs):
        self.host_url = kwargs['host_url']
        self.api_key = kwargs['api_key']
        self.instance_name = kwargs['instance_name']

    @abstractmethod
    def update(self):
        raise(f'{self.__class__.__name__} class has not implemented function update.')
    
class BaseTransmissionClass(BaseTorrentClass):
    TYPE = MateyType.TRANSMISSION
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from transmission_rpc import Client
        self.api = Client(self.host_url, self.api_key)
        self.api._http_session = kwargs['verify'] # TODO: Using private attribute
        
class BaseQbittorrentClass(BaseTorrentClass):
    TYPE = MateyType.QBITTORRENT
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from qbittorrent import Client
        self.api = Client(self.host_url, self.api_key, verify=kwargs['verify'])
        self.api.login(kwargs['username'], self.api_key)