from matey_exporter.common import BaseMateyClass


class BaseTorrentClass(BaseMateyClass):
    
    def __init__(self, client, **kwargs):
        super().__init__(**kwargs)
        self.api = client
