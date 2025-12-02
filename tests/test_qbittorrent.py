import pytest
from matey_exporter.torrent import load_qbittorrent_full, load_qbittorrent_simple
from matey_exporter.torrent.qbittorrent_simple import MateyQbittorrentSimple, MateyQbittorrentPrometheusMetricsSimple
from matey_exporter.torrent.qbittorrent_full import MateyQbittorrentFull, MateyQbittorrentPrometheusMetricsFull

good_test_config_1 = {
    "qbittorrent": [
        {"host_url": "http://192.168.1.100:8989",
         "api_key": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
         "instance_name": "qbittorrent-one",
        }
    ],
}
good_test_config_2 = {
    "qbittorrent": [
        {"host_url": "http://192.168.1.100:8989",
         "api_key": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
         "instance_name": "qbittorrent-two",
        }
    ],
}

def test_good_config_qbittorrent_simple():
    qbittorrent = load_qbittorrent_simple(**good_test_config_1['qbittorrent'][0])
    assert isinstance(qbittorrent, MateyQbittorrentSimple)
    assert qbittorrent.metrics is MateyQbittorrentPrometheusMetricsSimple()
    assert qbittorrent.instance_name == "qbittorrent-one"
    assert qbittorrent.host_url == "http://192.168.1.100:8989"
    assert qbittorrent.api_key == "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    
def test_qbittorrent_metrics_singleton_simple():
    qbittorrent_1 = load_qbittorrent_simple(**good_test_config_1['qbittorrent'][0])
    qbittorrent_2 = load_qbittorrent_simple(**good_test_config_2['qbittorrent'][0])
    assert qbittorrent_1.metrics is qbittorrent_2.metrics
    
def test_good_config_qbittorrent_full():
    qbittorrent = load_qbittorrent_full(**good_test_config_1['qbittorrent'][0])
    assert isinstance(qbittorrent, MateyQbittorrentFull)
    assert qbittorrent.metrics is MateyQbittorrentPrometheusMetricsFull()
    assert qbittorrent.instance_name == "qbittorrent-one"
    assert qbittorrent.host_url == "http://192.168.1.100:8989"
    assert qbittorrent.api_key == "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    
def test_qbittorrent_metrics_singleton_full():
    qbittorrent_1 = load_qbittorrent_full(**good_test_config_1['qbittorrent'][0])
    qbittorrent_2 = load_qbittorrent_full(**good_test_config_2['qbittorrent'][0])
    assert qbittorrent_1.metrics is qbittorrent_2.metrics