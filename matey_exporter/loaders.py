
# __init__ loaders from submodules
from matey_exporter.starr import starr_loader
from matey_exporter.torrent import torrent_loader

loaders_dict = {
    **starr_loader, 
    **torrent_loader,
}