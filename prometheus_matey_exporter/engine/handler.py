

class MateyHandler:
    
    def __init__(self, *args, **kwargs):
        self.sources = []
        
    def add_source(self, source):
        self.sources.append(source)
        
    def remove_source(self, source):
        self.sources.pop(source)