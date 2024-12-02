import pytest
from unittest.mock import MagicMock

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

mock_client = MagicMock()
mock_client.username = 'test_user'
mock_client.password = 'test_password'


def test_good_config_transmission(mocker):
    
    # Patch 'transmission_rpc.Client' to return our mock instead of the real Client
    mocker.patch('transmission_rpc.Client', return_value=mock_client)
    from matey_exporter.torrent.transmission import MateyTransmission, MateyTransmissionPrometheusMetrics
    
    transmission = MateyTransmission(**good_test_config_1['transmission'][0])
    assert isinstance(transmission, MateyTransmission)
    assert transmission.metrics is MateyTransmissionPrometheusMetrics()
    assert transmission.instance_name == "transmission-one"
    assert transmission.host_url == "http://192.168.1.100:8989"
    assert transmission.api_key == "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    
def test_transmission_metrics_singleton(mocker):
    
    # Patch 'transmission_rpc.Client' to return our mock instead of the real Client
    mocker.patch('transmission_rpc.Client', return_value=mock_client)
    from matey_exporter.torrent.transmission import MateyTransmission
    
    transmission_1 = MateyTransmission(**good_test_config_1['transmission'][0])
    transmission_2 = MateyTransmission(**good_test_config_2['transmission'][0])
    assert transmission_1.instance_name == "transmission-one"
    assert transmission_2.instance_name == "transmission-two"
    assert transmission_1.metrics is transmission_2.metrics
