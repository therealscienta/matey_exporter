import pytest
from matey_exporter.torrent import load_transmission
from matey_exporter.torrent.transmission import MateyTransmission, transmission_metrics
good_test_config_1 = {
    "transmission": [
        {"host_url": "http://192.168.1.100:8989",
         "api_key": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
         "instance_name": "transmission-one",
        }
    ],
}
good_test_config_2 = {
    "transmission": [
        {"host_url": "http://192.168.1.100:8989",
         "api_key": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
         "instance_name": "transmission-two",
        }
    ],
}

def test_good_config_transmission():
    transmission = load_transmission(**good_test_config_1['transmission'][0])
    assert isinstance(transmission, MateyTransmission)
    assert transmission.metrics is transmission_metrics
    assert transmission.instance_name == "transmission-one"
    assert transmission.host_url == "http://192.168.1.100:8989"
    assert transmission.api_key == "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    
def test_transmission_metrics_singleton():
    transmission_1 = load_transmission(**good_test_config_1['transmission'][0])
    transmission_2 = load_transmission(**good_test_config_2['transmission'][0])
    assert transmission_1.metrics is transmission_2.metrics