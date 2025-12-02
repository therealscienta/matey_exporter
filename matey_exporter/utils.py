
import sys
import yaml
from yaml.loader import SafeLoader
from pathlib import Path
from schema import Schema, Or

from matey_exporter.common.log import logger
from matey_exporter.loaders import matey_loaders, matey_schemas
from matey_exporter.common.exceptions import MateyYamlConfigValidationError


def get_config(file_path: Path) -> dict[str]:
    '''
    Load yaml config file from supplied path and return dictionary.
    '''
    
    try:
        with open(file_path.as_posix()) as f:
            config = yaml.load(f, Loader=SafeLoader)
        logger.debug(f'Config file loaded: {file_path}')
    
    except Exception as e:
        logger.critical(f'Could not load config file: {e}')
        sys.exit('Exiting.')
    if validate_yaml_config(config): return config


def validate_yaml_config(config: dict[str]) -> bool:
    '''
    Validate the config file against a schema and return 
    True if valid, or exit with an error message if not.
    '''

    combined_schema = Schema({
        Or(*matey_schemas.get('services')): Or(*matey_schemas.get('schemas'))
    })
        
    try:
        combined_schema.validate(config)
        logger.debug('Configuration is valid.')
    except Exception as e:
        raise MateyYamlConfigValidationError(e)
    return True


def disable_https_warnings(sources_set: set) -> None:
    '''
    This is a workaround for the requests library to disable TLS verification warnings.
    Default behavior is to verify TLS certificates.
    '''
    if False in sources_set:
        from requests.packages import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    


def load_sources(config: dict[str]) -> set:
    '''
    Function that dynamically loads the correct datasource type.
    '''
    
    sources = set()
    
    for datasource, instance_configs in config.items():
        for cfg in instance_configs:
            sources.add(matey_loaders[datasource][cfg.get('mode', 'simple')](**cfg))
    
    disable_https_warnings((source.verify for source in sources))
    return sources
