
starr_loader = {
    'sonarr': lambda **kwargs: 
        load_sonarr(**kwargs),
    
    'radarr': lambda **kwargs: 
        load_radarr(**kwargs),
    
    'lidarr': lambda **kwargs: 
        load_lidarr(**kwargs),
}

def load_sonarr(**kwargs):
    from .sonarr import MateySonarr
    return MateySonarr(**kwargs)

def load_radarr(**kwargs):
    from .radarr import MateyRadarr
    return MateyRadarr(**kwargs)
    
def load_lidarr(url, api_key, instance_name):
    pass