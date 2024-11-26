from matey_exporter.common import BaseMateyClass


class BaseTorrentClass(BaseMateyClass):
    
    def __init__(self, client=None, **kwargs): #TODO: Rework inheritance
        super().__init__(**kwargs)
        self.api = client
