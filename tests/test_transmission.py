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


def test_good_config_transmission_simple(mocker):
    
    # Patch 'transmission_rpc.Client' to return our mock instead of the real Client
    mocker.patch('transmission_rpc.Client', return_value=mock_client)
    from matey_exporter.torrent.transmission_simple import MateyTransmissionSimple, MateyTransmissionPrometheusMetricsSimple
    
    transmission = MateyTransmissionSimple(**good_test_config_1['transmission'][0])
    assert isinstance(transmission, MateyTransmissionSimple)
    assert transmission.metrics is MateyTransmissionPrometheusMetricsSimple()
    assert transmission.instance_name == "transmission-one"
    assert transmission.host_url == "http://192.168.1.100:8989"
    assert transmission.api_key == "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    
def test_transmission_metrics_singleton_simple(mocker):
    
    # Patch 'transmission_rpc.Client' to return our mock instead of the real Client
    mocker.patch('transmission_rpc.Client', return_value=mock_client)
    from matey_exporter.torrent.transmission_simple import MateyTransmissionSimple
    
    transmission_1 = MateyTransmissionSimple(**good_test_config_1['transmission'][0])
    transmission_2 = MateyTransmissionSimple(**good_test_config_2['transmission'][0])
    assert transmission_1.instance_name == "transmission-one"
    assert transmission_2.instance_name == "transmission-two"
    assert transmission_1.metrics is transmission_2.metrics
    
def test_good_config_transmission_full(mocker):
    
    # Patch 'transmission_rpc.Client' to return our mock instead of the real Client
    mocker.patch('transmission_rpc.Client', return_value=mock_client)
    from matey_exporter.torrent.transmission_full import MateyTransmissionFull, MateyTransmissionPrometheusMetricsFull
    
    transmission = MateyTransmissionFull(**good_test_config_1['transmission'][0])
    assert isinstance(transmission, MateyTransmissionFull)
    assert transmission.metrics is MateyTransmissionPrometheusMetricsFull()
    assert transmission.instance_name == "transmission-one"
    assert transmission.host_url == "http://192.168.1.100:8989"
    assert transmission.api_key == "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    
def test_transmission_metrics_singleton_full(mocker):
    
    # Patch 'transmission_rpc.Client' to return our mock instead of the real Client
    mocker.patch('transmission_rpc.Client', return_value=mock_client)
    from matey_exporter.torrent.transmission_full import MateyTransmissionFull
    
    transmission_1 = MateyTransmissionFull(**good_test_config_1['transmission'][0])
    transmission_2 = MateyTransmissionFull(**good_test_config_2['transmission'][0])
    assert transmission_1.instance_name == "transmission-one"
    assert transmission_2.instance_name == "transmission-two"
    assert transmission_1.metrics is transmission_2.metrics
