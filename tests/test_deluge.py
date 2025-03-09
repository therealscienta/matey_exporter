import pytest
from matey_exporter.torrent import load_deluge_full, load_deluge_simple
from matey_exporter.torrent.deluge_simple import MateyDelugeSimple, MateyDelugePrometheusMetricsSimple
from matey_exporter.torrent.deluge_full import MateyDelugeFull, MateyDelugePrometheusMetricsFull

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

# def test_good_config_deluge_simple():
#     deluge = load_deluge_simple(**good_test_config_1['deluge'][0])
#     assert isinstance(deluge, MateyDelugeSimple)
#     assert deluge.metrics is MateyDelugePrometheusMetricsSimple()
#     assert deluge.instance_name == "deluge-one"
#     assert deluge.host_url == "http://192.168.1.100:8989"
#     assert deluge.password == "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    
# def test_deluge_metrics_singleton_simple():
#     deluge_1 = load_deluge_simple(**good_test_config_1['deluge'][0])
#     deluge_2 = load_deluge_simple(**good_test_config_2['deluge'][0])
#     assert deluge_1.metrics is deluge_2.metrics
    
def test_good_config_deluge_full():
    deluge = load_deluge_full(**good_test_config_1['deluge'][0])
    assert isinstance(deluge, MateyDelugeFull)
    assert deluge.metrics is MateyDelugePrometheusMetricsFull()
    assert deluge.instance_name == "deluge-one"
    assert deluge.host_url == "http://192.168.1.100:8989"
    assert deluge.password == "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    
def test_deluge_metrics_singleton_full():
    deluge_1 = load_deluge_full(**good_test_config_1['deluge'][0])
    deluge_2 = load_deluge_full(**good_test_config_2['deluge'][0])
    assert deluge_1.metrics is deluge_2.metrics