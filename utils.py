
import sys

from prometheus_matey_exporter.starr import starr_loader
from prometheus_matey_exporter.torrent import torrent_loader



def load_submodules(config, handler) -> None:
    """ Function that dynamically tries to load the correct datasource type. """
    
    # __init__ loaders from submodules
    loaders = {
        **starr_loader, 
        **torrent_loader,
    }
    
    try:
        for datasource in config.keys(): # sonarr/radarr etc.
            for config_instance in config[datasource.lower()]:
                
                # Disable request TLS verify warning
                if 'verify' in config_instance.keys() and config_instance['verify'] == False:
                    from requests.packages import urllib3
                    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                else:
                    config_instance['verify'] = True
                
                # Add sources to handler
                handler.add_source(
                    loaders[datasource](
                        **config_instance))
    except Exception as e:
        sys.exit(f'Invalid configuration option in: {datasource} - {e}')



class MateyHandler:
    
    def __init__(self):
        self.sources = set()
        
    def add_source(self, source):
        self.sources.add(source)
        
    def remove_source(self, source):
        self.sources.remove(source)