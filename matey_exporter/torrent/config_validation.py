from schema import Schema, Optional, Or

transmission_schema = Schema([{
        'host_url': str,
        'instance_name': str,
        'username': str,
        'password': str,
        Optional('verify'): bool,
        Optional('mode'): Or('simple', 'full'),
    }])

qbittorrent_schema = Schema([{
        'host_url': str,
        Optional('port'): int,
        'instance_name': str,
        'username': str,
        'password': str,
        Optional('verify'): bool,
        Optional('mode'): Or('simple', 'full'),
    }])

deluge_schema = Schema([{
        'host_url': str,
        'instance_name': str,
        Optional('username'): str,
        'password': str,
        Optional('verify'): bool,
        Optional('mode'): Or('simple', 'full'),
    }])

torrent_schemas = {
    'schemas': [transmission_schema, 
                qbittorrent_schema, 
                deluge_schema],
    'services': ['Transmission', 
                'Deluge', 
                'Qbittorrent']
    }