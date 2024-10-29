


torrent_loader = {
    'transmission': lambda **kwargs: 
        load_tranmission(**kwargs),
        
    'qbittorrent': lambda **kwargs: 
        load_qbittorrent(**kwargs),
}


def load_tranmission(**kwargs):
    from .transmission import MateyTransmission
    return MateyTransmission(**kwargs)

def load_qbittorrent(**kwargs):
    from .qbittorrent import MateyQbittorrent
    return MateyQbittorrent(**kwargs)