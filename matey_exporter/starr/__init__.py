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
    'Sonarr': {'simple': load_sonarr,
               'full': load_sonarr},
    'Radarr': {'simple': load_radarr,
               'full': load_radarr},
    'Lidarr': {'simple': load_lidarr,
               'full': load_lidarr},
    'Readar': {'simple': load_readarr,
               'full': load_readarr}
}
