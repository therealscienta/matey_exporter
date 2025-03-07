from .config_validation import starr_schemas

def load_sonarr(**kwargs):
    from .sonarr import MateySonarr
    return MateySonarr(**kwargs)

def load_radarr(**kwargs):
    from .radarr import MateyRadarr
    return MateyRadarr(**kwargs)
    
def load_lidarr(**kwargs):
    from .lidarr import MateyLidarr
    return MateyLidarr(**kwargs)

def load_readarr(**kwargs):
    from .readarr import MateyReadarr
    return MateyReadarr(**kwargs)

starr_loader = {
    'Sonarr': load_sonarr,
    'Radarr': load_radarr,
    'Lidarr': load_lidarr,
    'Readar': load_readarr,
}
