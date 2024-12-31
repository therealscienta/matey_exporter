
from matey_exporter.common.base import BaseMateyClass

class BaseStarrClass(BaseMateyClass):
    
    def __init__(self, api, **kwargs):
        super().__init__(**kwargs)
        self.api = api(self.host_url, self.api_key)
        self.api.session.verify = kwargs.get('verify')
