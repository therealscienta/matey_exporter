
import re
import sys
import yaml
from yaml.loader import SafeLoader
from pathlib import Path
from schema import Optional, Schema, Or
from typing import Any

from matey_exporter.common import logger
from .loaders import loaders_dict


def get_config(file_path: Path) -> dict[str]:
    '''Load yaml config file from supplied path and return dictionary.'''
    
    try:
        with open(file_path.as_posix()) as f:
            config = yaml.load(f, Loader=SafeLoader)
        logger.debug(f'Config file loaded:  {file_path}')
    
    except Exception as e:
        logger.critical(f'Could not load config file: {e}')
        sys.exit('Exiting.')
    if validate_yaml_config(config): return config


def validate_yaml_config(config: dict[str]) -> bool:
    '''
    Validate the config file against a schema and return 
    True if valid, or exit with an error message if not.
    '''

    # Regex for validating config file
    regex_url = re.compile(r"^https?:\/\/")
    # regex_api_key = re.compile(r"^[a-zA-Z0-9]{32}$") 
    # TODO: Add regex for api_key and password to schema
    # for validation and/or verify non example config

    # Load available datasource types to use for schema evaluation
    datasources_schema_evalutation = set(key.capitalize() for key in loaders_dict.keys())

    config_schema = Schema({
        Or(*datasources_schema_evalutation): [{
            'host_url': lambda str: regex_url.match(str),
            'instance_name': str,
            Or('api_key', 'password', only_one=True): str, #lambda str: regex_api_key.match(str),
            Optional('username'): str,
            Optional('verify'): bool,
            },
        ],
    })

    try:
        config_schema.validate(config)
        logger.debug('Configuration is valid.')
        return True
    except Exception as e:
        e = re.sub(r"'api_key': '\S*',", '', str(e)) # Remove api_key from logging output
        e = re.sub(r"'password': '\S*',", '', str(e)) # Remove password from logging output
        try:
            instance = e.splitlines()[1].split()[-3] # Get instance name from error message.
            error = e.splitlines()[-2]
        except IndexError:
            instance = 'Unknown'
            error = e
        logger.critical(f'Configuration is invalid: {error} {instance}')
        sys.exit('Exiting.')
        
        
def tls_verify_check(config_instance: dict[str]) -> dict:
    '''
    Check if TLS verify is set to False, or set it to True if not set.
    This is a workaround for the requests library to disable TLS verification warnings.
    Default behavior is to verify TLS certificates.
    '''

    if config_instance.get('verify') == False:
        from requests.packages import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    else:
        config_instance.update(verify=True)
    return config_instance
    


def load_sources(config: dict[str]) -> set:
    '''Function that dynamically loads the correct datasource type.'''
    
    sources = set()
    
    # TODO: Rework nested for loops
    for datasource, instance_configs in config.items():
        for config in instance_configs:
            sources.add(loaders_dict[datasource](**tls_verify_check(config)))
    return sources
