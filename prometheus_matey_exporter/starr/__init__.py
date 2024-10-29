
starr_loader = {
    'sonarr': lambda url, api_key, instance_name: 
        load_sonarr(url, api_key, instance_name),
     
     'radarr': lambda url, api_key, instance_name: 
        load_radarr(url, api_key, instance_name),
     
     'lidarr': lambda url, api_key, instance_name: 
        load_lidarr(url, api_key, instance_name),
}

def load_sonarr(url, api_key, instance_name):
    from .sonarr import MateySonarr
    return MateySonarr(url, api_key, instance_name)

def load_radarr(url, api_key, instance_name):
    pass
    
def load_lidarr(url, api_key, instance_name):
    pass