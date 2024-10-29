


torrent_loader = {
    'transmission': lambda url, api_key, instance_name: 
        load_tranmission(url, api_key, instance_name),
        
    'qbittorrent': lambda url, api_key, instance_name: 
        load_qbittorrent(url, api_key, instance_name),
}


def load_tranmission(url, api_key, instance_name):
    from .transmission import MateyTransmission
    return MateyTransmission(url, api_key, instance_name)

def load_qbittorrent(url, api_key, instance_name):
    from .qbittorrent import MateyQbittorrent
    return MateyQbittorrent(url, api_key, instance_name)