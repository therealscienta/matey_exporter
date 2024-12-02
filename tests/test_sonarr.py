import pytest
from matey_exporter.starr import load_sonarr
from matey_exporter.starr.sonarr import MateySonarr, MateySonarrPrometheusMetrics
good_test_config_1 = {
    "Sonarr": [
        {"host_url": "http://192.168.1.100:8989",
         "api_key": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
         "instance_name": "sonarr-one",
        }
    ],
}
good_test_config_2 = {
    "Sonarr": [
        {"host_url": "http://192.168.1.100:8989",
         "api_key": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
         "instance_name": "sonarr-two",
        }
    ],
}

def test_good_config_sonarr():
    sonarr = load_sonarr(**good_test_config_1['Sonarr'][0])
    assert isinstance(sonarr, MateySonarr)
    assert sonarr.metrics is MateySonarrPrometheusMetrics()
    assert sonarr.instance_name == "sonarr-one"
    assert sonarr.host_url == "http://192.168.1.100:8989"
    assert sonarr.api_key == "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    
def test_sonarr_metrics_singleton():
    sonarr_1 = load_sonarr(**good_test_config_1['Sonarr'][0])
    sonarr_2 = load_sonarr(**good_test_config_2['Sonarr'][0])
    assert sonarr_1.metrics is sonarr_2.metrics