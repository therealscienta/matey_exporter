

def load_tranmission(**kwargs):
    from torrent.transmission import MateyTransmission
    return MateyTransmission(**kwargs)

def load_qbittorrent(**kwargs):
    from torrent.qbittorrent import MateyQbittorrent
    return MateyQbittorrent(**kwargs)

torrent_loader = {
    'Transmission': load_tranmission,
    'Qbittorrent': load_qbittorrent,
}