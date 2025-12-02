
import pytest
from matey_exporter.utils import validate_yaml_config
from matey_exporter.common.exceptions import MateyYamlConfigValidationError

good_test_config = {
        "Sonarr": [
            {
                "host_url": "http://192.168.1.100:8989",
                "api_key": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                "instance_name": "sonarr",
                "verify": False
            }
        ],
        "Radarr": [
            {
                "host_url": "http://192.168.1.101",
                "api_key": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                "instance_name": "radarr-one",
                "verify": False
            },
            {
                "host_url": "http://radarr.local.net",
                "api_key": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                "instance_name": "radarr-two",
                "verify": True
            }
        ]}

bad_test_config_1 = {
        "Radarr": [
            {
                "url": "http://192.168.1.100:7878",
                "api_key": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                "instance_name": "radarr",
                "verify": False
            }
        ]}

bad_test_config_2 = {
        "sonarr": [
            {
                "host_url": "http://192.168.1.100:8989",
                "api_key": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                "instance_name": "sonarr",
                "verify": False
            }
        ]}

def test_good_validate_yaml_config():
    assert validate_yaml_config(good_test_config) == True

def test_bad_validate_yaml_config():
    with pytest.raises(MateyYamlConfigValidationError):
        assert validate_yaml_config(bad_test_config_1)
    with pytest.raises(MateyYamlConfigValidationError):
        assert validate_yaml_config(bad_test_config_2)