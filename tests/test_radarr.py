import pytest
from matey_exporter.starr import load_radarr
from matey_exporter.starr.radarr import MateyRadarr, MateyRadarrPrometheusMetrics
good_test_config_1 = {
    "radarr": [
        {"host_url": "http://192.168.1.100:8989",
         "api_key": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
         "instance_name": "radarr-one",
        }
    ],
}
good_test_config_2 = {
    "radarr": [
        {"host_url": "http://192.168.1.100:8989",
         "api_key": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
         "instance_name": "radarr-two",
        }
    ],
}

def test_good_config_radarr():
    radarr = load_radarr(**good_test_config_1['radarr'][0])
    assert isinstance(radarr, MateyRadarr)
    assert radarr.metrics is MateyRadarrPrometheusMetrics()
    assert radarr.instance_name == "radarr-one"
    assert radarr.host_url == "http://192.168.1.100:8989"
    assert radarr.api_key == "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    
def test_radarr_metrics_singleton():
    radarr_1 = load_radarr(**good_test_config_1['radarr'][0])
    radarr_2 = load_radarr(**good_test_config_2['radarr'][0])
    assert radarr_1.metrics is radarr_2.metrics