import pytest
from matey_exporter.torrent import load_deluge
from matey_exporter.torrent.deluge import MateyDeluge, MateyDelugePrometheusMetrics

good_test_config_1 = {
    "deluge": [
        {"host_url": "http://192.168.1.100:8989",
         "password": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
         "instance_name": "deluge-one",
        }
    ],
}
good_test_config_2 = {
    "deluge": [
        {"host_url": "http://192.168.1.100:8989",
         "password": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
         "instance_name": "deluge-two",
        }
    ],
}

def test_good_config_deluge():
    deluge = load_deluge(**good_test_config_1['deluge'][0])
    assert isinstance(deluge, MateyDeluge)
    assert deluge.metrics is MateyDelugePrometheusMetrics()
    assert deluge.instance_name == "deluge-one"
    assert deluge.host_url == "http://192.168.1.100:8989"
    assert deluge.password == "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    
def test_deluge_metrics_singleton():
    deluge_1 = load_deluge(**good_test_config_1['deluge'][0])
    deluge_2 = load_deluge(**good_test_config_2['deluge'][0])
    assert deluge_1.metrics is deluge_2.metrics