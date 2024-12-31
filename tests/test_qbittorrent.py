import pytest
from matey_exporter.torrent import load_qbittorrent
from matey_exporter.torrent.qbittorrent import MateyQbittorrent, MateyQbittorrentPrometheusMetrics

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

def test_good_config_qbittorrent():
    qbittorrent = load_qbittorrent(**good_test_config_1['qbittorrent'][0])
    assert isinstance(qbittorrent, MateyQbittorrent)
    assert qbittorrent.metrics is MateyQbittorrentPrometheusMetrics()
    assert qbittorrent.instance_name == "qbittorrent-one"
    assert qbittorrent.host_url == "http://192.168.1.100:8989"
    assert qbittorrent.api_key == "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    
def test_qbittorrent_metrics_singleton():
    qbittorrent_1 = load_qbittorrent(**good_test_config_1['qbittorrent'][0])
    qbittorrent_2 = load_qbittorrent(**good_test_config_2['qbittorrent'][0])
    assert qbittorrent_1.metrics is qbittorrent_2.metrics