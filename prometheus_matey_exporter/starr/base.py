from abc import ABC, abstractmethod

class StarrClass(ABC):
    
    def __init__(self, host_url, api_key, instance_name): #TODO
        self.url = host_url
        self.api_key = api_key
        self.instance_name = instance_name
        self.api = None

    @abstractmethod
    def update(self):
        pass