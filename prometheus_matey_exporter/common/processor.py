from abc import ABC, abstractmethod

class DataProcessorBase(ABC):
    
    @abstractmethod
    def get_data(cls):
        """ Main processor method to process fetched data and turn into Promethus metrics. """
        raise(f'{cls.__class__.__name__} class has not implemented function get_data.')