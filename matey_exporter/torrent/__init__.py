

def load_transmission(**kwargs):
    from .transmission import MateyTransmission
    return MateyTransmission(**kwargs)

def load_qbittorrent(**kwargs):
    from .qbittorrent import MateyQbittorrent
    return MateyQbittorrent(**kwargs)

def load_deluge(**kwargs):
    from .deluge import MateyDeluge
    return MateyDeluge(**kwargs)

torrent_loader = {
    'Transmission': load_transmission,
    'Qbittorrent': load_qbittorrent,
    'Deluge': load_deluge,
}