from schema import Schema, Optional

transmission_schema = Schema([{
        'host_url': str,
        'instance_name': str,
        'username': str,
        'password': str,
        Optional('verify'): bool,
    }])

qbittorrent_schema = Schema([{
        'host_url': str,
        'instance_name': str,
        'username': str,
        'password': str,
        Optional('verify'): bool,
    }])

deluge_schema = Schema([{
        'host_url': str,
        'instance_name': str,
        Optional('username'): str,
        'password': str,
        Optional('verify'): bool,
    }])

torrent_schemas = {
    'schemas': [transmission_schema, 
                qbittorrent_schema, 
                deluge_schema],
    'services': ['Transmission', 
                'Deluge', 
                'Qbittorrent']
    }