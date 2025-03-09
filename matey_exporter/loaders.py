
# __init__ loaders from submodules
from matey_exporter.starr import starr_loader, starr_schemas
from matey_exporter.torrent import torrent_loader, torrent_schemas

matey_loaders = {
    **starr_loader, 
    **torrent_loader,
}

matey_schemas = {
    'schemas': 
        starr_schemas.get('schemas') + 
        torrent_schemas.get('schemas'),
    'services': 
        starr_schemas.get('services') + 
        torrent_schemas.get('services'),
}
