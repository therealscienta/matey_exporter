from .config_validation import torrent_schemas

def load_transmission_simple(**kwargs):
    from .transmission_simple import MateyTransmissionSimple
    return MateyTransmissionSimple(**kwargs)

def load_qbittorrent_simple(**kwargs):
    from .qbittorrent_simple import MateyQbittorrentSimple
    return MateyQbittorrentSimple(**kwargs)

def load_deluge_simple(**kwargs):
    from .deluge_simple import MateyDelugeSimple
    return MateyDelugeSimple(**kwargs)

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
        'simple': load_transmission_simple,
        'full': load_transmission_full
    },
    'Qbittorrent': {
        'simple': load_qbittorrent_simple,
        'full': load_qbittorrent_full
    },
    'Deluge': { # TODO: change to deluge simple, when implemented
        'simple': load_deluge_full,
        'full': load_deluge_full
    },
}

