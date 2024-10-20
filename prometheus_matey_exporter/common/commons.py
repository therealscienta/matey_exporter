
from enum import Enum

class MateyType(Enum):
    SONARR = 'sonarr'
    RADARR = 'radarr'
    LIDARR = 'lidarr'
    READARR = 'readarr'
    QBITTORRENT = 'qbittorrent'
    TRANSMISSION = 'transmission'
    UTORRENT = 'utorrent'
    SABNZBD = 'sabnzbd'