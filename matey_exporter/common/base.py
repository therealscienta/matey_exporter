from abc import ABC, abstractmethod

class BaseMateyClass(ABC):
    
    def __init__(self, **kwargs):
        self.host_url = kwargs.get('host_url')
        self.api_key = kwargs.get('api_key') # TODO: Securely store api_key?
        self.instance_name = kwargs.get('instance_name')
        
    @abstractmethod
    def query_and_process_data(self):
        raise(f'{self.__class__.__name__} class has not implemented function update.')