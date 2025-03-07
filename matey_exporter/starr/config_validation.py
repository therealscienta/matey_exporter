from schema import Schema, Optional
import re

regex_api_key = re.compile(r"^[a-zA-Z0-9]{32}$")

starr_schema = Schema([{
    'host_url': str,
    'instance_name': str,
    'api_key': lambda str: regex_api_key.match(str),
    Optional('verify'): bool,
    }])


starr_schemas = {
    'schemas': [starr_schema],
    'services': ['Sonarr', 'Radarr', 'Lidarr', 'Readarr']
    }