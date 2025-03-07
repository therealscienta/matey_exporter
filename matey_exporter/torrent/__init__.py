
from .config_validation import torrent_schemas

def load_transmission(**kwargs):
    from .transmission_simple import MateyTransmission
    return MateyTransmission(**kwargs)

def load_qbittorrent(**kwargs):
    from .qbittorrent_simple import MateyQbittorrent
    return MateyQbittorrent(**kwargs)

def load_deluge(**kwargs):
    from .deluge_simple import MateyDeluge
    return MateyDeluge(**kwargs)

def load_transmission_full(**kwargs):
    from .transmission_full import MateyTransmissionFull
    return MateyTransmissionFull(**kwargs)

def load_qbittorrent_full(**kwargs):
    from .qbittorrent_full import MateyQbittorrentFull
    return MateyQbittorrentFull(**kwargs)

def load_deluge_full(**kwargs):
    from .deluge_full import MateyDelugeFull
    return MateyDelugeFull(**kwargs)

torrent_loader = {
    'Transmission': {
        'simple': load_transmission,
        'full': load_transmission_full
    },
    'Qbittorrent': {
        'simple': load_qbittorrent,
        'full': load_qbittorrent_full
    },
    'Deluge': {
        'simple': load_deluge,
        'full': load_deluge_full
    },
}

